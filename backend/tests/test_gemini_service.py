from unittest.mock import Mock, patch

from pydantic import ValidationError

from app.ai.parsers.schemas import CandidateSummary
from app.ai.services.gemini_service import GeminiService


def test_generate_structured_returns_pydantic_model():
    fake_response = Mock()
    fake_response.text = '{"name": "John Smith", "skills": ["Python", "FastAPI"]}'

    with patch.object(
        GeminiService,
        "__init__",
        return_value=None,
    ):
        service = GeminiService()

    service.client = Mock()
    service.model = "gemini-3.6-flash"

    service.client.models.generate_content.return_value = fake_response

    result = service.generate_structured(
        "Extract candidate information",
        CandidateSummary,
    )

    assert isinstance(result, CandidateSummary)
    assert result.name == "John Smith"
    assert result.skills == ["Python", "FastAPI"]


def test_generate_structured_rejects_invalid_response():
    fake_response = Mock()
    fake_response.text = '{"name": "John Smith", "skill": ["Python", "FastAPI"]}'

    with patch.object(
        GeminiService,
        "__init__",
        return_value=None,
    ):
        service = GeminiService()

    service.client = Mock()
    service.model = "gemini-3.6-flash"

    service.client.models.generate_content.return_value = fake_response

    try:
        service.generate_structured(
            "Extract candidate information",
            CandidateSummary
        )
        assert False, "Expected Pydantic ValidationError"
    except ValidationError:
        assert True