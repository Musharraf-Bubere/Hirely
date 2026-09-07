from uuid import UUID

from pydantic import BaseModel


class MatchingInput(BaseModel):
    candidate_id: UUID
    candidate_skills: list[str]
    required_skills: list[str]
    preferred_skills: list[str] | None = None
    candidate_embedding: list[float]
    job_embedding: list[float]