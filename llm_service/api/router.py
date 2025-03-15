from fastapi import APIRouter, HTTPException
from typing import Dict

from ..core.config import settings, LLMProvider
from ..providers.openai_provider import OpenAIProvider
from ..providers.deepseek_provider import DeepseekProvider
from ..providers.local_provider import LocalProvider
from .models import AnalyzeRequest, AnalyzeResponse


router = APIRouter()

# Provider mapping
PROVIDERS: Dict[LLMProvider, type] = {
    LLMProvider.OPENAI: OpenAIProvider,
    LLMProvider.DEEPSEEK: DeepseekProvider,
    LLMProvider.LOCAL: LocalProvider,
}


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_function(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze a Python function using the configured LLM provider.
    """
    provider_class = PROVIDERS.get(settings.LLM_PROVIDER)
    if not provider_class:
        raise HTTPException(
            status_code=501, detail=f"Provider {settings.LLM_PROVIDER} not implemented"
        )

    try:
        provider = provider_class()
        suggestions = await provider.analyze_function(request.function_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )

    return AnalyzeResponse(suggestions=suggestions)
