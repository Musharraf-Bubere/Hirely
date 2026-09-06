from uuid import UUID

from pydantic import BaseModel

from app.ai.parsers.schemas import ResumeData

from app.ai.embeddings.service import EmbeddingService
from app.ai.representations.candidate import (
    CandidateRepresentation,
    CandidateRepresentationBuilder
)



class CandidatePreparationInput(BaseModel):
    candidate_id: UUID
    resume_data: ResumeData


class CandidatePreparationResult(BaseModel):
    candidate_id: UUID
    representation: CandidateRepresentation
    embedding: list[float]


class CandidatePreparationService:
    def __init__(
        self,
        representation_builder: CandidateRepresentationBuilder,
        embedding_service: EmbeddingService,
    ):
        self.representation_builder = representation_builder
        self.embedding_service = embedding_service

    def prepare(
        self,
        data: CandidatePreparationInput,
    ) -> CandidatePreparationResult:
        representation = self.representation_builder.build(
            data.resume_data
        )

        embedding = self.embedding_service.embed_text(
            representation.profile_text
        )

        return CandidatePreparationResult(
            candidate_id=data.candidate_id,
            representation=representation,
            embedding=embedding,
        )