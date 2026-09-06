from uuid import UUID

from app.ai.representations.job import JobRepresentation
from app.ai.services.job_preparation_service import (
    JobPreparationInput,
    JobPreparationService,
)


class FakeJobRepresentationBuilder:
    def build(
        self,
        title,
        description,
        location=None,
        employment_type=None,
        experience_level=None,
        required_skills=None,
        preferred_skills=None,
    ):
        return JobRepresentation(
            job_text="Job Profile\n\nTitle:\nAI Engineer"
        )


class FakeEmbeddingService:
    def __init__(self):
        self.received_text = None

    def embed_text(self, text):
        self.received_text = text
        return [0.1, 0.2, 0.3]


def test_job_preparation_service_builds_representation_and_embedding():
    job_id = UUID("11111111-1111-1111-1111-111111111111")

    data = JobPreparationInput(
        job_id=job_id,
        title="AI Engineer",
        description="Build AI applications",
        required_skills=["Python", "FastAPI"],
        preferred_skills=["AWS"],
    )

    service = JobPreparationService(
        representation_builder=FakeJobRepresentationBuilder(),
        embedding_service=FakeEmbeddingService(),
    )

    result = service.prepare(data)

    assert result.job_id == job_id
    assert result.representation.job_text == (
        "Job Profile\n\nTitle:\nAI Engineer"
    )
    assert result.embedding == [0.1, 0.2, 0.3]

def test_job_preparation_service_passes_representation_text_to_embedding():
    job_id = UUID("11111111-1111-1111-1111-111111111111")

    data = JobPreparationInput(
        job_id=job_id,
        title="AI Engineer",
        description="Build AI applications",
        required_skills=["Python", "FastAPI"],
        preferred_skills=["AWS"],
    )

    fake_embedding_service = FakeEmbeddingService()

    service = JobPreparationService(
        representation_builder=FakeJobRepresentationBuilder(),
        embedding_service=fake_embedding_service,
    )

    service.prepare(data)

    assert fake_embedding_service.received_text == (
        "Job Profile\n\nTitle:\nAI Engineer"
    )