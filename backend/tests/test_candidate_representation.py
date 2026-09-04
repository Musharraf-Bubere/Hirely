from app.ai.parsers.schemas import (
    Certification,
    Education,
    Project,
    ResumeData,
    WorkExperience,
)
from app.ai.representations.candidate import (
    CandidateRepresentationBuilder,
)


def test_candidate_representation_builder():
    resume_data = ResumeData(
        name="John Smith",
        location="Mumbai, India",
        headline="Data Analyst",
        summary="Data analyst with experience in business intelligence.",
        skills=["Python", "SQL", "Power BI"],
        experience=[
            WorkExperience(
                company="ABC Technologies",
                job_title="Data Analyst",
                start_date="2023",
                end_date="2025",
                description="Analyzed business data using Python and SQL.",
            )
        ],
        projects=[
            Project(
                name="Sales Dashboard",
                description="Built a sales analytics dashboard.",
                technologies=["Power BI", "DAX"],
            )
        ],
        education=[
            Education(
                institution="XYZ University",
                degree="Bachelor of Commerce",
                field_of_study="Business Analytics",
                end_date="2022",
            )
        ],
        certifications=[
            Certification(
                name="Data Analysis with Python",
                issuer="IBM",
                date="2025",
            )
        ],
    )

    builder = CandidateRepresentationBuilder()

    result = builder.build(resume_data)

    assert result.profile_text

    assert "Candidate Profile" in result.profile_text
    assert "Location:\nMumbai, India" in result.profile_text
    assert "Headline:\nData Analyst" in result.profile_text
    assert "Summary:\nData analyst with experience in business intelligence." in result.profile_text
    assert "Skills:\nPython, SQL, Power BI" in result.profile_text

    assert "Data Analyst at ABC Technologies" in result.profile_text
    assert "2023 - 2025" in result.profile_text
    assert "Analyzed business data using Python and SQL." in result.profile_text

    assert "Sales Dashboard" in result.profile_text
    assert "Built a sales analytics dashboard." in result.profile_text
    assert "Technologies: Power BI, DAX" in result.profile_text

    assert "Bachelor of Commerce" in result.profile_text
    assert "XYZ University" in result.profile_text
    assert "Field of Study: Business Analytics" in result.profile_text

    assert "Data Analysis with Python" in result.profile_text
    assert "Issuer: IBM" in result.profile_text
    assert "Date: 2025" in result.profile_text


def test_candidate_representation_omits_empty_sections():
    resume_data = ResumeData(
        location="Mumbai, India",
        summary="Data analyst with experience in data analysis.",
        skills=["Python", "SQL"],
        experience=[],
        projects=[],
        education=[],
        certifications=[],
    )

    builder = CandidateRepresentationBuilder()

    result = builder.build(resume_data)

    assert "Candidate Profile" in result.profile_text
    assert "Location:\nMumbai, India" in result.profile_text
    assert "Summary:\nData analyst with experience in data analysis." in result.profile_text
    assert "Skills:\nPython, SQL" in result.profile_text

    assert "Professional Experience:" not in result.profile_text
    assert "Projects:" not in result.profile_text
    assert "Education:" not in result.profile_text
    assert "Certifications:" not in result.profile_text