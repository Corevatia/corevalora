from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    MARKETSTACK_API_KEY: str
    COINCAP_API_KEY: Optional[str] = None
    DEV_MODE: bool = False
    UPSTREAM_DEBUG: bool = False
    LOGGING_LEVEL: str = "INFO"
    DB_URL: str

    model_config = SettingsConfigDict(env_file=Path(__file__).parent / '../.env', env_file_encoding='utf-8')


settings = Settings()
