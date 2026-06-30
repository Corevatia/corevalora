from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    MARKETSTACK_API_KEY: str
    COINCAP_API_KEY: str
    MOCK_DATA: bool = False
    UPSTREAM_DEBUG: bool = False
    LOGGING_LEVEL: str = "INFO"
    POSTGRES_USER: str = "corevalora"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "corevalora"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: str = "5432"
    SESSION_LIFETIME_DAYS: int = 14
    COOKIE_SECURE: bool = False
    CORS_ORIGINS: str = "http://localhost:5173"
    CRYPTO_CACHE_TTL_SECONDS: Optional[int] = 120
    STOCK_CACHE_TTL_HOURS: Optional[int] = 24
    SEARCH_CACHE_TTL_HOURS: Optional[int] = 48
    MAINTENANCE_LOOP_HOURS: Optional[int] = 6

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[2] / '.env',
        env_file_encoding='utf-8')


    @property
    def DB_URL(self) -> str:
        return(
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
