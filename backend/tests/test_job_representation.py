from app.ai.representations.job import JobRepresentationBuilder


def test_job_representation_builder():
    builder = JobRepresentationBuilder()

    result = builder.build(
        title="Backend Python Developer",
        description="Build scalable REST APIs for our recruitment platform.",
        location="Mumbai, India",
        employment_type="Full-time",
        experience_level="Mid-level",
        required_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
        ],
        preferred_skills=[
            "Docker",
            "AWS",
        ],
    )

    assert result.job_text

    assert "Job Profile" in result.job_text
    assert "Title:\nBackend Python Developer" in result.job_text
    assert "Description:\nBuild scalable REST APIs for our recruitment platform." in result.job_text
    assert "Location:\nMumbai, India" in result.job_text
    assert "Employment Type:\nFull-time" in result.job_text
    assert "Experience Level:\nMid-level" in result.job_text

    assert "Required Skills:\nPython, FastAPI, PostgreSQL" in result.job_text
    assert "Preferred Skills:\nDocker, AWS" in result.job_text


def test_job_representation_omits_empty_sections():
    builder = JobRepresentationBuilder()

    result = builder.build(
        title="Python Developer",
        description="Build backend services.",
        required_skills=["Python"],
    )

    assert "Job Profile" in result.job_text
    assert "Title:\nPython Developer" in result.job_text
    assert "Description:\nBuild backend services." in result.job_text
    assert "Required Skills:\nPython" in result.job_text

    assert "Location:" not in result.job_text
    assert "Employment Type:" not in result.job_text
    assert "Experience Level:" not in result.job_text
    assert "Preferred Skills:" not in result.job_text