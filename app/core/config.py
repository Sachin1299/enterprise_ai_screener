import os
from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Enterprise Application Settings.
    Loads and validates environment variables at startup using Pydantic Settings.
    Fails fast if critical configurations are missing or malformed.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    # Core Application Settings
    app_name: str = "Enterprise-Candidate-Intelligence-Screener"
    app_env: str = "development"
    debug: bool = True
    port: int = 8000
    host: str = "0.0.0.0"

    # Google Gemini LLM & Embedding Settings
    gemini_api_key: str = Field(default="", description="Google Gemini API Key")
    gemini_model: str = "gemini-2.5-flash"
    embedding_model: str = "models/text-embedding-004"

    # Storage & Persistence
    chroma_persist_directory: str = "./data/chroma_db"
    upload_directory: str = "./data/uploads"

    # Langfuse Observability & Tracing
    langfuse_public_key: Optional[str] = None
    langfuse_secret_key: Optional[str] = None
    langfuse_host: str = "https://cloud.langfuse.com"

    # Agent Safeguards & Operational Limits
    max_recursion_limit: int = 10
    default_strictness: str = "balanced"
    log_level: str = "INFO"

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in ("production", "prod")

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() in ("development", "dev")

    @property
    def has_langfuse(self) -> bool:
        return bool(self.langfuse_public_key and self.langfuse_secret_key)


@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the application settings.
    Ensures .env is read and validated once rather than on every request.
    """
    return Settings()
