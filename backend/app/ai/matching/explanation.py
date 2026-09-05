from uuid import UUID

from pydantic import BaseModel, Field


class MatchExplanationInput(BaseModel):
    candidate_id: UUID

    overall_score: float = Field(ge=0.0, le=1.0)

    required_skill_score: float = Field(ge=0.0, le=1.0)
    preferred_skill_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )
    semantic_similarity: float = Field(ge=0.0, le=1.0)

    required_matched: list[str]
    required_missing: list[str]

    preferred_matched: list[str]
    preferred_missing: list[str]


class MatchExplanationEvidence(BaseModel):
    required_skill_score: float = Field(ge=0.0, le=1.0)

    preferred_skill_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
    )

    semantic_similarity: float = Field(ge=0.0, le=1.0)


class MatchExplanation(BaseModel):
    summary: str = Field(min_length=1)

    strengths: list[str]

    gaps: list[str]

    evidence: MatchExplanationEvidence

    caveats: list[str]