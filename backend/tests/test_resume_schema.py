from app.ai.parsers.schemas import ResumeData


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