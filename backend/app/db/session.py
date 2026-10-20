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
    - SQLite engines (used in lightweight tests or embedded modes) do not support QueuePool
      and are excluded from these arguments to avoid configuration errors.
    - Sizing: Total active database connections across the deployment equals:
      (pool_size + max_overflow) * number_of_worker_processes.
      Ensure this product does not exceed PostgreSQL's configured `max_connections` (minus superuser reservations).
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
