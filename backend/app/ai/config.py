from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]


class AISettings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-3.6-flash"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


ai_settings = AISettings()