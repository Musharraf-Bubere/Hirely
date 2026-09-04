import pytest

from app.ai.embeddings.service import EmbeddingService
from app.ai.parsers.schemas import ResumeData
from app.ai.representations.candidate import CandidateRepresentationBuilder


@pytest.mark.integration
def test_candidate_representation_can_be_embedded():
    resume_data = ResumeData(
        name="John Smith",
        location="Mumbai, India",
        headline="Python Backend Developer",
        summary="Backend developer experienced in building APIs and data-driven applications.",
        skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
        ],
    )

    representation_builder = CandidateRepresentationBuilder()
    representation = representation_builder.build(resume_data)

    embedding_service = EmbeddingService()
    embedding = embedding_service.embed_text(
        representation.profile_text
    )

    assert representation.profile_text
    assert isinstance(embedding, list)
    assert len(embedding) == 768
    assert all(isinstance(value, float) for value in embedding)