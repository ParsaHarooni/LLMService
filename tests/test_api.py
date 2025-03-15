import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from llm_service.main import app


MOCK_RESPONSE = """{"suggestions": [
    "Add type hints to improve code clarity",
    "Add docstring for better documentation"
]}"""


@pytest.fixture
def client():
    return TestClient(app)


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


def test_analyze_endpoint(client, mock_openai_response):
    response = client.post(
        "/analyze", json={"function_code": "def add(a, b): return a + b"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)
