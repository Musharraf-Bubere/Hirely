import pytest

from app.ai.embeddings.service import EmbeddingService
from app.ai.representations.job import JobRepresentationBuilder


@pytest.mark.integration
def test_job_representation_can_be_embedded():
    representation_builder = JobRepresentationBuilder()

    representation = representation_builder.build(
        title="Backend Python Developer",
        description=(
            "Build scalable REST APIs and backend services "
            "for our recruitment platform."
        ),
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

    embedding_service = EmbeddingService()

    embedding = embedding_service.embed_text(
        representation.job_text
    )

    assert representation.job_text
    assert isinstance(embedding, list)
    assert len(embedding) == 768
    assert all(isinstance(value, float) for value in embedding)