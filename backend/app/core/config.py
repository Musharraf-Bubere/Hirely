from pathlib import Path
from typing import Any

from pydantic import field_validator, model_validator
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

    # Storage configuration: "local" (default) or "r2"
    storage_backend: str = "local"
    resume_storage_dir: str = "app/storage/resumes"
    r2_account_id: str | None = None
    r2_access_key_id: str | None = None
    r2_secret_access_key: str | None = None
    r2_bucket_name: str | None = None
    r2_endpoint_url: str | None = None

    @property
    def computed_r2_endpoint_url(self) -> str | None:
        if self.r2_endpoint_url:
            return self.r2_endpoint_url
        if self.r2_account_id:
            return f"https://{self.r2_account_id}.r2.cloudflarestorage.com"
        return None

    @field_validator("storage_backend")
    @classmethod
    def validate_storage_backend(cls, v: str) -> str:
        backend = (v or "").strip().lower()
        if backend not in {"local", "r2"}:
            raise ValueError(
                f"Unsupported STORAGE_BACKEND: '{v}'. Only 'local' and 'r2' are accepted."
            )
        return backend

    @model_validator(mode="after")
    def validate_storage_settings(self) -> "Settings":
        backend = (self.storage_backend or "").strip().lower()
        if backend not in {"local", "r2"}:
            raise ValueError(
                f"Unsupported STORAGE_BACKEND: '{self.storage_backend}'. Only 'local' and 'r2' are accepted."
            )
        if backend == "r2":
            missing = []
            if not self.r2_access_key_id:
                missing.append("R2_ACCESS_KEY_ID")
            if not self.r2_secret_access_key:
                missing.append("R2_SECRET_ACCESS_KEY")
            if not self.r2_bucket_name:
                missing.append("R2_BUCKET_NAME")
            if not self.r2_endpoint_url and not self.r2_account_id:
                missing.append("R2_ENDPOINT_URL or R2_ACCOUNT_ID")
            if missing:
                raise ValueError(
                    f"R2 storage backend is configured, but required parameters are missing: {', '.join(missing)}"
                )
        return self

    # Database connection pool configuration
    # Note: pool capacity (db_pool_size + db_max_overflow) is allocated per worker process.
    # Formula: maximum connections = (db_pool_size + db_max_overflow) * worker processes
    # Default: (5 + 10) * 4 Uvicorn workers = 60 connections, comfortably within PostgreSQL's
    # default max_connections (100) and leaving 40 connections for superuser reservations (3),
    # Alembic migrations, and operational buffers.
    db_pool_size: int = 5
    db_max_overflow: int = 10
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
