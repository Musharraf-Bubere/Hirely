from unittest.mock import patch

from app.core.config import Settings
from app.db.session import create_database_engine


def test_database_pool_settings_defaults():
    # Instantiate Settings without env file overrides
    settings = Settings(
        database_url="postgresql+psycopg://test:test@localhost:5432/test",
        jwt_secret_key="test-secret-key-at-least-32-chars-long",
        _env_file=None,
    )
    assert settings.db_pool_size == 10
    assert settings.db_max_overflow == 20
    assert settings.db_pool_timeout == 30
    assert settings.db_pool_recycle == 1800
    assert settings.db_pool_pre_ping is True


def test_sqlite_engine_compatibility():
    """Ensure SQLite in-memory and file engines do not receive incompatible QueuePool arguments."""
    engine = create_database_engine("sqlite:///:memory:")
    # Should connect cleanly without TypeError: Invalid argument(s) 'pool_size'
    with engine.connect() as conn:
        result = conn.exec_driver_sql("SELECT 1").scalar()
        assert result == 1


def test_postgresql_engine_pool_arguments():
    """Ensure PostgreSQL engines receive bounded connection pool configurations."""
    with patch("app.db.session.create_engine") as mock_create_engine:
        create_database_engine("postgresql+psycopg://user:pass@localhost:5432/hirely")
        mock_create_engine.assert_called_once()
        args, kwargs = mock_create_engine.call_args
        assert args[0] == "postgresql+psycopg://user:pass@localhost:5432/hirely"
        assert kwargs["pool_pre_ping"] is True
        assert kwargs["pool_size"] == 10
        assert kwargs["max_overflow"] == 20
        assert kwargs["pool_timeout"] == 30
        assert kwargs["pool_recycle"] == 1800
