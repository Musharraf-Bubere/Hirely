from app.ai.parsers.schemas import ResumeData
from app.ai.services.gemini_service import gemini_service


def test_gemini_can_parse_resume_text():
    resume_text = """
    John Smith
    Email: john.smith@example.com
    Phone: +91 9876543210
    Location: Mumbai, India

    Python Backend Developer

    Summary:
    Backend developer with 3 years of experience building REST APIs
    and backend systems.

    Skills:
    Python, FastAPI, PostgreSQL, Docker, Git

    Experience:
    Software Engineer at ABC Technologies
    January 2023 - Present
    Built REST APIs using FastAPI and PostgreSQL.

    Education:
    B.Tech in Computer Science
    XYZ University
    2019 - 2023
    """

    prompt = f"""
    Extract structured candidate information from the following resume.

    Return only information explicitly present in the resume.
    Do not invent or infer missing information.

    Resume:
    {resume_text}
    """

    result = gemini_service.generate_structured(
        prompt,
        ResumeData,
    )

    assert isinstance(result, ResumeData)
    assert result.name == "John Smith"
    assert result.email == "john.smith@example.com"
    assert "Python" in result.skills
    assert "FastAPI" in result.skills
    assert len(result.experience) >= 1
    assert len(result.education) >= 1