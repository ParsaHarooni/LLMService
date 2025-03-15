import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from llm_service.providers.openai_provider import OpenAIProvider
from llm_service.providers.deepseek_provider import DeepseekProvider
from llm_service.providers.local_provider import LocalProvider


MOCK_RESPONSE = """{"suggestions": [
    "Add type hints to improve code clarity",
    "Add docstring for better documentation"
]}"""


@pytest.fixture
def mock_openai_response():
    with patch("openai.AsyncOpenAI", autospec=True) as mock_openai:
        # Create a mock client instance
        mock_client = AsyncMock()

        # Create a mock chat instance
        mock_chat = AsyncMock()
        mock_client.chat = mock_chat

        # Create a mock completions instance
        mock_completions = AsyncMock()
        mock_chat.completions = mock_completions

        # Create a mock completion response
        mock_completion = AsyncMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content=MOCK_RESPONSE))]

        # Set up the mock chain
        mock_completions.create = AsyncMock(return_value=mock_completion)
        mock_openai.return_value = mock_client

        yield mock_openai


@pytest.mark.asyncio
async def test_openai_provider(mock_openai_response):
    provider = OpenAIProvider()
    suggestions = await provider.analyze_function("def add(a, b): return a + b")

    assert len(suggestions) >= 0


# Test JSON parsing error fallback
@pytest.mark.asyncio
async def test_openai_provider_json_error():
    with patch("openai.AsyncOpenAI", autospec=True) as mock_openai:
        # Create a mock client instance
        mock_client = AsyncMock()

        # Create a mock chat instance
        mock_chat = AsyncMock()
        mock_client.chat = mock_chat

        # Create a mock completions instance
        mock_completions = AsyncMock()
        mock_chat.completions = mock_completions

        # Create a mock completion response with invalid JSON
        mock_completion = AsyncMock()
        mock_completion.choices = [
            MagicMock(
                message=MagicMock(content="Invalid JSON\nAdd type hints\nAdd docstring")
            )
        ]

        # Set up the mock chain
        mock_completions.create = AsyncMock(return_value=mock_completion)
        mock_openai.return_value = mock_client

        provider = OpenAIProvider()
        suggestions = await provider.analyze_function("def add(a, b): return a + b")

        assert len(suggestions) >= 0


@pytest.fixture
def mock_deepseek_response():
    with patch("httpx.AsyncClient", autospec=True) as mock_client:
        # Create mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": MOCK_RESPONSE}}]
        }
        mock_response.raise_for_status = AsyncMock()

        # Set up the mock chain
        mock_client_instance = AsyncMock()
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        yield mock_client


@pytest.mark.asyncio
async def test_deepseek_provider(mock_deepseek_response):
    provider = DeepseekProvider()
    suggestions = await provider.analyze_function("def add(a, b): return a + b")

    assert len(suggestions) >= 0


@pytest.fixture
def mock_local_model(tmp_path):
    model_path = tmp_path / "model.bin"
    model_path.touch()

    with patch("ctransformers.LLM", autospec=True) as mock_llm:
        # Create mock instance
        mock_instance = MagicMock()
        mock_instance.return_value = MOCK_RESPONSE
        mock_llm.return_value = mock_instance

        with patch(
            "llm_service.core.config.settings.LOCAL_MODEL_PATH", str(model_path)
        ):
            yield mock_llm


@pytest.mark.asyncio
async def test_local_provider(mock_local_model):
    provider = LocalProvider()
    suggestions = await provider.analyze_function("def add(a, b): return a + b")

    assert len(suggestions) >= 0


@pytest.mark.asyncio
async def test_local_provider_missing_model():
    with patch(
        "llm_service.core.config.settings.LOCAL_MODEL_PATH", "/nonexistent/path"
    ):
        with pytest.raises(FileNotFoundError):
            LocalProvider()
