from unittest.mock import Mock

from app.ai.parsers.resume_parser import ResumeParserService
from app.ai.parsers.schemas import ResumeData


def test_resume_parser_returns_structured_resume_data():
    fake_ai_service = Mock()

    expected_result = ResumeData(
        name="John Smith",
        email="john@example.com",
        skills=["Python", "FastAPI"],
    )

    fake_ai_service.generate_structured.return_value = expected_result

    parser = ResumeParserService(ai_service=fake_ai_service)

    resume_text = """
    John Smith
    Email: john@example.com

    Python Backend Developer

    Skills:
    Python, FastAPI
    """

    result = parser.parse(resume_text)

    assert isinstance(result, ResumeData)
    assert result.name == "John Smith"
    assert result.email == "john@example.com"
    assert result.skills == ["Python", "FastAPI"]

    fake_ai_service.generate_structured.assert_called_once()