from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from enum import Enum
from typing import Optional


class LLMProvider(str, Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    LOCAL = "local"


class Settings(BaseSettings):
    # LLM Provider configuration
    LLM_PROVIDER: LLMProvider = LLMProvider.OPENAI

    # OpenAI settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Deepseek settings
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-chat-v3"

    # Local LLM settings
    LOCAL_MODEL_PATH: Optional[str] = None

    model_config = ConfigDict(env_file=".env", use_enum_values=True)


settings = Settings()
