from pathlib import Path

from app.ai.parsers.resume_parser import ResumeParserService


RESUME_PATH = (
    Path(__file__).resolve().parent.parent
    / "test_data"
    / "Musharraf_Resume.pdf"
)


def test_real_resume_pipeline():
    parser = ResumeParserService()

    result = parser.parse_file(RESUME_PATH)

    assert result.name == "Musharraf Bubere"
    assert result.email == "musharrafbubere007@gmail.com"
    assert result.phone == "+91 93705 20445"

    assert len(result.skills) > 0
    assert "Python" in result.skills
    assert "SQL" in result.skills

    assert len(result.projects) > 0
    assert any(
        project.name == "HR Data Analytics Dashboard"
        for project in result.projects
    )

    assert len(result.certifications) > 0
    assert any(
        "Data Analysis with Python" in certification.name
        for certification in result.certifications
    )

    assert len(result.education) > 0
    assert any(
        education.institution == "IT Vedant - Private Institute"
        for education in result.education
    )

    assert result.experience == []