from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str
    API_KEY_HMAC_PEPPER: str
    DATABASE_URL: str
    REDIS_URL: str
    DEFAULT_FAIL_MODE: str = "FAIL_CLOSED"
    MAX_PAYLOAD_SIZE_BYTES: int = 262144
    HITL_DEFAULT_TTL_SECONDS: int = 900
    NEXT_PUBLIC_API_BASE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()