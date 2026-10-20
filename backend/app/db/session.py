from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


def create_database_engine(database_url: str | None = None) -> Engine:
    """
    Construct a SQLAlchemy Engine with bounded connection pooling.

    Operational notes:
    - Queue pool arguments (pool_size, max_overflow, pool_timeout, pool_recycle) are applied
      to production RDBMS drivers such as PostgreSQL.
    - SQLite engines (used in tests or embedded modes) do not support QueuePool
      and are excluded from these arguments to avoid configuration errors.
    - Connection budgeting formula:
      maximum connections = (pool_size + max_overflow) * worker processes
      With default pool_size=5 and max_overflow=10 across 4 Uvicorn workers:
      (5 + 10) * 4 = 60 maximum application connections.
      This fits comfortably within PostgreSQL's default max_connections=100 limit,
      leaving 40 connections for superuser reservations (default 3), Alembic migrations,
      and operational headroom.
    """
    url = database_url or settings.database_url
    engine_kwargs: dict[str, Any] = {
        "pool_pre_ping": settings.db_pool_pre_ping,
    }

    # Only apply QueuePool parameters to non-SQLite databases (e.g. PostgreSQL)
    if not url.startswith("sqlite"):
        engine_kwargs.update(
            {
                "pool_size": settings.db_pool_size,
                "max_overflow": settings.db_max_overflow,
                "pool_timeout": settings.db_pool_timeout,
                "pool_recycle": settings.db_pool_recycle,
            }
        )

    return create_engine(url, **engine_kwargs)


engine = create_database_engine()


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
