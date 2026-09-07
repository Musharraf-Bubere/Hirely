from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest
from google.genai import errors
from pydantic import ValidationError

from app.ai.parsers.schemas import ResumeData
from app.ai.services.gemini_service import GeminiService


def create_test_service():
    with patch.object(
        GeminiService,
        "__init__",
        return_value=None,
    ):
        service = GeminiService()

    service.client = Mock()
    service.model = "gemini-3.5-flash-lite"
    service.fallback_model = "gemini-3.5-flash"

    return service


def test_generate_structured_returns_pydantic_model():
    service = create_test_service()

    fake_response = Mock()
    fake_response.text = (
        '{"name": "John Smith", '
        '"skills": ["Python", "FastAPI"]}'
    )

    service.client.models.generate_content.return_value = fake_response

    result = service.generate_structured(
        "Extract candidate information",
        ResumeData,
    )

    assert isinstance(result, ResumeData)
    assert result.name == "John Smith"
    assert result.skills == ["Python", "FastAPI"]


def test_generate_structured_rejects_invalid_response():
    service = create_test_service()

    fake_response = Mock()
    fake_response.text = (
        '{"name": 123, '
        '"skills": "Python"}'
    )

    service.client.models.generate_content.return_value = fake_response

    with pytest.raises(ValidationError):
        service.generate_structured(
            "Extract candidate information",
            ResumeData,
        )


def test_generate_text_uses_fallback_on_503(monkeypatch):
    service = create_test_service()

    calls = []

    def fake_generate_content(
        *,
        model,
        prompt,
        config=None,
    ):
        calls.append(model)

        if len(calls) == 1:
            raise errors.ServerError(
                503,
                {
                    "error": {
                        "code": 503,
                        "message": "Temporary unavailable",
                        "status": "UNAVAILABLE",
                    }
                },
            )

        return SimpleNamespace(
            text="fallback response"
        )

    monkeypatch.setattr(
        service,
        "_generate_content",
        fake_generate_content,
    )

    result = service.generate_text("test prompt")

    assert result == "fallback response"

    assert calls == [
        service.model,
        service.fallback_model,
    ]


def test_generate_text_does_not_use_fallback_for_non_503(
    monkeypatch,
):
    service = create_test_service()

    calls = []

    def fake_generate_content(
        *,
        model,
        prompt,
        config=None,
    ):
        calls.append(model)

        raise errors.ClientError(
            400,
            {
                "error": {
                    "code": 400,
                    "message": "Bad request",
                    "status": "INVALID_ARGUMENT",
                }
            },
        )

    monkeypatch.setattr(
        service,
        "_generate_content",
        fake_generate_content,
    )

    with pytest.raises(errors.ClientError):
        service.generate_text("test prompt")

    assert calls == [service.model]