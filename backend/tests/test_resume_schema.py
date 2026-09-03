from app.ai.parsers.schemas import (
    Certification,
    Education,
    Project,
    ResumeData,
)


def test_resume_data_accepts_complete_resume():
    data = ResumeData(
        name="John Smith",
        email="john@example.com",
        phone="1234567890",
        location="Mumbai, India",
        headline="Python Developer",
        summary="Backend developer with experience building APIs.",
        skills=["Python", "FastAPI", "PostgreSQL"],
        experience=[
            {
                "company": "ABC Technologies",
                "job_title": "Software Engineer",
                "start_date": "2023-01",
                "end_date": "Present",
                "description": "Built backend APIs using FastAPI.",
            }
        ],
        education=[
            {
                "institution": "XYZ University",
                "degree": "B.Tech",
                "field_of_study": "Computer Science",
                "start_date": "2019",
                "end_date": "2023",
            }
        ],
    )

    assert data.name == "John Smith"
    assert data.skills == ["Python", "FastAPI", "PostgreSQL"]
    assert len(data.experience) == 1
    assert len(data.education) == 1


def test_resume_data_allows_missing_optional_fields():
    data = ResumeData(
        name="Jane Doe",
        skills=["Python"],
    )

    assert data.name == "Jane Doe"
    assert data.email is None
    assert data.phone is None
    assert data.experience == []
    assert data.education == []


def test_resume_data_supports_projects_and_certifications():
    resume = ResumeData(
        name="Musharraf Bubere",
        skills=["Python", "SQL"],
        projects=[
            Project(
                name="HR Data Analytics Dashboard",
                description="Built an interactive HR analytics dashboard.",
                technologies=["Power BI", "DAX"],
            )
        ],
        certifications=[
            Certification(
                name="Data Analysis with Python",
                issuer="IBM",
                date="Nov 2025",
            )
        ],
        education=[
            Education(
                institution="IT Vedant - Private Institute",
                degree="Master's",
                field_of_study="Data Science, Analytics & Artificial Intelligence",
                end_date="2025",
            )
        ],
    )

    assert resume.projects[0].name == "HR Data Analytics Dashboard"
    assert resume.projects[0].technologies == ["Power BI", "DAX"]

    assert resume.certifications[0].name == "Data Analysis with Python"
    assert resume.certifications[0].issuer == "IBM"

    assert resume.education[0].institution == "IT Vedant - Private Institute"