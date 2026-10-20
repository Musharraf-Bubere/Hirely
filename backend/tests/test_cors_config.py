from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from app.core.config import Settings


def test_cors_config_defaults():
    # Verify model field default debug is False and development localhost is configured
    assert Settings.model_fields["debug"].default is False

    test_settings = Settings(
        _env_file=None,
        database_url="postgresql+psycopg://test:test@localhost:5432/test",
        jwt_secret_key="a" * 32,
    )

    assert test_settings.debug is False
    assert "http://localhost:5173" in test_settings.cors_origins
    assert "http://127.0.0.1:5173" in test_settings.cors_origins


def test_cors_config_comma_separated_parsing():
    test_settings = Settings(
        _env_file=None,
        database_url="postgresql+psycopg://test:test@localhost:5432/test",
        jwt_secret_key="a" * 32,
        cors_origins="https://hirely.com, https://app.hirely.com, https://api.hirely.com",
    )

    assert test_settings.cors_origins == [
        "https://hirely.com",
        "https://app.hirely.com",
        "https://api.hirely.com",
    ]


def test_cors_config_json_list_parsing():
    test_settings = Settings(
        _env_file=None,
        database_url="postgresql+psycopg://test:test@localhost:5432/test",
        jwt_secret_key="a" * 32,
        cors_origins='["https://staging.hirely.com", "https://prod.hirely.com"]',
    )

    assert test_settings.cors_origins == [
        "https://staging.hirely.com",
        "https://prod.hirely.com",
    ]


def test_cors_middleware_disables_credentials_on_wildcard():
    # Create test app with wildcard origins
    app = FastAPI()
    cors_origins = ["*"]
    has_wildcard = "*" in cors_origins
    allow_credentials = False if has_wildcard else True

    assert allow_credentials is False

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/test")
    def get_test():
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/test", headers={"Origin": "https://malicious.com"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "*"
    # access-control-allow-credentials must NEVER be 'true' when origin is wildcard
    assert response.headers.get("access-control-allow-credentials") is None


def test_cors_middleware_preserves_credentials_on_explicit_origin():
    app = FastAPI()
    cors_origins = ["https://app.hirely.com"]
    has_wildcard = "*" in cors_origins
    allow_credentials = False if has_wildcard else True

    assert allow_credentials is True

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/test")
    def get_test():
        return {"ok": True}

    client = TestClient(app)
    response = client.get("/test", headers={"Origin": "https://app.hirely.com"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "https://app.hirely.com"
    assert response.headers.get("access-control-allow-credentials") == "true"
