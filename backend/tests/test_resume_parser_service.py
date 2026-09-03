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


def test_parse_file_uses_resume_loader():
    mock_ai_service = Mock()
    mock_ai_service.generate_structured.return_value = ResumeData(
        name="Musharraf Bubere",
        skills=["Python", "SQL"],
    )

    mock_resume_loader = Mock()
    mock_resume_loader.load_text.return_value = (
        "Musharraf Bubere\n"
        "Skills: Python, SQL"
    )

    parser = ResumeParserService(
        ai_service=mock_ai_service,
        resume_loader=mock_resume_loader,
    )

    result = parser.parse_file("resume.pdf")

    mock_resume_loader.load_text.assert_called_once_with("resume.pdf")
    mock_ai_service.generate_structured.assert_called_once()

    assert result.name == "Musharraf Bubere"
    assert result.skills == ["Python", "SQL"]