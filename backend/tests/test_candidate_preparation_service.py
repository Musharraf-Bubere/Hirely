from uuid import UUID

from app.ai.parsers.schemas import ResumeData
from app.ai.representations.candidate import CandidateRepresentation
from app.ai.services.candidate_preparation_service import (
    CandidatePreparationInput,
    CandidatePreparationService,
)


class FakeRepresentationBuilder:
    def build(self, resume_data):
        return CandidateRepresentation(
            profile_text="Candidate Profile\n\nSkills:\nPython"
        )


class FakeEmbeddingService:
    def __init__(self):
        self.received_text = None

    def embed_text(self, text):
        self.received_text = text
        return [0.1, 0.2, 0.3]


def test_candidate_preparation_service_builds_representation_and_embedding():
    candidate_id = UUID("11111111-1111-1111-1111-111111111111")

    resume_data = ResumeData(
        name="Test Candidate",
        skills=["Python"],
    )

    service = CandidatePreparationService(
        representation_builder=FakeRepresentationBuilder(),
        embedding_service=FakeEmbeddingService(),
    )

    data = CandidatePreparationInput(
        candidate_id=candidate_id,
        resume_data=resume_data,
    )

    result = service.prepare(data)

    assert result.candidate_id == candidate_id
    assert result.representation.profile_text == (
        "Candidate Profile\n\nSkills:\nPython"
    )
    assert result.embedding == [0.1, 0.2, 0.3]

def test_candidate_preparation_service_passes_representation_text_to_embedding():
    candidate_id = UUID("11111111-1111-1111-1111-111111111111")

    resume_data = ResumeData(
        name="Test Candidate",
        skills=["Python"],
    )

    fake_embedding_service = FakeEmbeddingService()

    service = CandidatePreparationService(
        representation_builder=FakeRepresentationBuilder(),
        embedding_service=fake_embedding_service,
    )

    data = CandidatePreparationInput(
        candidate_id=candidate_id,
        resume_data=resume_data,
    )

    service.prepare(data)

    assert fake_embedding_service.received_text == (
        "Candidate Profile\n\nSkills:\nPython"
    )