from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]


class AISettings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-3.5-flash-lite"
    gemini_fallback_model: str = "gemini-3.5-flash"

    # Configurable Gemini generation output token bounds per feature
    default_max_output_tokens: int = 2048
    resume_parser_max_tokens: int = 3072
    cover_letter_max_tokens: int = 2048
    career_coach_max_tokens: int = 2048
    resume_improvement_max_tokens: int = 2048
    ats_analyzer_max_tokens: int = 1536
    job_description_max_tokens: int = 1536
    rag_max_tokens: int = 1536
    match_explanation_max_tokens: int = 1024

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


ai_settings = AISettings()
