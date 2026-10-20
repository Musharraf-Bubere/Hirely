from unittest.mock import MagicMock, patch
from pydantic import BaseModel

from app.ai.config import ai_settings
from app.ai.services.gemini_service import GeminiService


class SampleResponseSchema(BaseModel):
    summary: str


def test_gemini_generate_text_default_max_output_tokens():
    service = GeminiService()
    mock_response = MagicMock()
    mock_response.text = "Sample output text"

    with patch.object(service, "_generate_with_fallback", return_value=mock_response) as mock_gen:
        result = service.generate_text("Test prompt")
        assert result == "Sample output text"
        mock_gen.assert_called_once_with(
            prompt="Test prompt",
            config={"max_output_tokens": ai_settings.default_max_output_tokens},
        )


def test_gemini_generate_text_custom_max_output_tokens():
    service = GeminiService()
    mock_response = MagicMock()
    mock_response.text = "Short text"

    with patch.object(service, "_generate_with_fallback", return_value=mock_response) as mock_gen:
        result = service.generate_text("Test prompt", max_output_tokens=512)
        assert result == "Short text"
        mock_gen.assert_called_once_with(
            prompt="Test prompt",
            config={"max_output_tokens": 512},
        )


def test_gemini_generate_structured_max_output_tokens():
    service = GeminiService()
    mock_response = MagicMock()
    mock_response.text = '{"summary": "Valid structured JSON"}'

    with patch.object(service, "_generate_with_fallback", return_value=mock_response) as mock_gen:
        result = service.generate_structured(
            prompt="Test structured prompt",
            response_schema=SampleResponseSchema,
            max_output_tokens=1024,
        )
        assert result.summary == "Valid structured JSON"
        mock_gen.assert_called_once_with(
            prompt="Test structured prompt",
            config={
                "response_mime_type": "application/json",
                "response_schema": SampleResponseSchema,
                "max_output_tokens": 1024,
            },
        )


def test_gemini_generate_structured_schema_specific_bounds():
    from app.ai.parsers.schemas import ResumeData
    from app.ai.matching.explanation import MatchExplanation

    service = GeminiService()
    mock_response = MagicMock()
    mock_response.text = '{"name": "Alice"}'

    with patch.object(service, "_generate_with_fallback", return_value=mock_response) as mock_gen:
        service.generate_structured(prompt="Resume prompt", response_schema=ResumeData)
        assert mock_gen.call_args.kwargs["config"]["max_output_tokens"] == ai_settings.resume_parser_max_tokens

    mock_response.text = '{"summary": "Match", "strengths": [], "gaps": [], "caveats": [], "evidence": {"required_skill_score": 1.0, "preferred_skill_score": 1.0, "semantic_similarity": 1.0}}'
    with patch.object(service, "_generate_with_fallback", return_value=mock_response) as mock_gen:
        service.generate_structured(prompt="Match prompt", response_schema=MatchExplanation)
        assert mock_gen.call_args.kwargs["config"]["max_output_tokens"] == ai_settings.match_explanation_max_tokens
