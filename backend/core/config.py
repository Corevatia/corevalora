from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    MARKETSTACK_API_KEY: str
    COINCAP_API_KEY: Optional[str] = None
    MOCK_DATA: bool = False
    UPSTREAM_DEBUG: bool = False
    LOGGING_LEVEL: str = "INFO"
    DB_URL: str
    SESSION_LIFETIME_DAYS: int = 14
    COOKIE_SECURE: bool = False
    CORS_ORIGINS: str = "http://localhost:5137"
    CRYPTO_CACHE_TTL_SECONDS: Optional[int] = 120
    STOCK_CACHE_TTL_HOURS: Optional[int] = 24
    SEARCH_CACHE_TTL_HOURS: Optional[int] = 48
    MAINTENANCE_LOOP_HOURS: Optional[int] = 6

    model_config = SettingsConfigDict(env_file=Path(__file__).parent / '../.env', env_file_encoding='utf-8')

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
