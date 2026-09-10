"""Centralized application configuration using Pydantic Settings.

All environment variables are loaded once at startup and accessed
through the singleton `get_settings()` function. This avoids scattered
`os.getenv()` calls throughout the codebase.
"""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # --- Application ---
    APP_NAME: str = "AI Video Studio"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # --- Authentication ---
    SECRET_KEY: str = "supersecretkey-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # --- Database ---
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_video_studio"

    # --- LLM (Prompt Enhancement) ---
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # --- Video Generation ---
    VIDEO_PROVIDER: str = "mock"
    VIDEO_MODEL: str = "fal-ai/kling-video/v3/pro/text-to-video"
    HF_TOKEN: str = ""

    # --- Timeouts & Retries ---
    GENERATION_TIMEOUT_SECONDS: int = 300
    MAX_RETRIES: int = 3
    RETRY_BASE_DELAY: float = 1.0

    # --- Prompt Limits ---
    MAX_PROMPT_LENGTH: int = 2000

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return [origin.strip() for origin in v.split(",")]
        return v


@lru_cache
def get_settings() -> Settings:
    """Return a cached singleton Settings instance."""
    return Settings()
