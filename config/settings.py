from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Dict, Optional
import os

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Marketing Agents API"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # OpenAI Settings
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str = "gpt-4o-mini"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TOP_P: float = 1.0
    OPENAI_FREQUENCY_PENALTY: float = 0.0
    OPENAI_PRESENCE_PENALTY: float = 0.0

    # LangChain Settings
    LANGCHAIN_VERBOSE: bool = False
    LANGCHAIN_DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_openai_config(self) -> Dict:
        """Get OpenAI configuration dictionary"""
        return {
            "model": self.OPENAI_MODEL_NAME,
            "temperature": self.OPENAI_TEMPERATURE,
            "max_tokens": self.OPENAI_MAX_TOKENS,
            "top_p": self.OPENAI_TOP_P,
            "frequency_penalty": self.OPENAI_FREQUENCY_PENALTY,
            "presence_penalty": self.OPENAI_PRESENCE_PENALTY,
        }

@lru_cache()
def get_settings() -> Settings:
    """
    Creates and returns a cached instance of the Settings class.
    The @lru_cache decorator ensures we only create one instance.
    """
    return Settings()