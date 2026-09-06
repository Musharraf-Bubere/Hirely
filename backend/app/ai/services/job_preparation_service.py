from uuid import UUID

from pydantic import BaseModel

from app.ai.representations.job import JobRepresentation
from app.ai.embeddings.service import EmbeddingService
from app.ai.representations.job import JobRepresentationBuilder


class JobPreparationInput(BaseModel):
    job_id: UUID
    title: str
    description: str
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None
    required_skills: list[str] = []
    preferred_skills: list[str] = []


class JobPreparationResult(BaseModel):
    job_id: UUID
    representation: JobRepresentation
    embedding: list[float]


class JobPreparationService:
    def __init__(
        self,
        representation_builder: JobRepresentationBuilder,
        embedding_service: EmbeddingService,
    ):
        self.representation_builder = representation_builder
        self.embedding_service = embedding_service

    def prepare(
        self,
        data: JobPreparationInput,
    ) -> JobPreparationResult:
        representation = self.representation_builder.build(
            title=data.title,
            description=data.description,
            location=data.location,
            employment_type=data.employment_type,
            experience_level=data.experience_level,
            required_skills=data.required_skills,
            preferred_skills=data.preferred_skills,
        )

        embedding = self.embedding_service.embed_text(
            representation.job_text
        )

        return JobPreparationResult(
            job_id=data.job_id,
            representation=representation,
            embedding=embedding,
        )