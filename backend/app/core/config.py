from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "Hirely API"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False
    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    # CORS configuration: default allowlist for local development
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Reverse proxy trust configuration: false by default
    trust_proxy_headers: bool = False

    # Database connection pool configuration
    # Note: pool capacity (db_pool_size + db_max_overflow) is per worker process.
    # Total connections to PostgreSQL = (db_pool_size + db_max_overflow) * workers.
    # Must be sized within PostgreSQL's max_connections limit.
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800
    db_pool_pre_ping: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [str(x).strip() for x in parsed if str(x).strip()]
                except Exception:
                    pass
            return [x.strip() for x in v.split(",") if x.strip()]
        elif isinstance(v, (list, tuple, set)):
            return [str(x).strip() for x in v if str(x).strip()]
        return []

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
