from uuid import UUID

from pydantic import BaseModel, Field

from app.ai.matching.scoring import MatchScoreResult
from app.ai.matching.skill_matching import SkillMatchResult
from app.ai.matching.explanation import MatchExplanation


class CompleteMatchResult(BaseModel):
    score: MatchScoreResult
    skills: SkillMatchResult


class RankedMatchResult(BaseModel):
    rank: int
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

class FinalMatchResult(BaseModel):
    match: RankedMatchResult
    explanation: MatchExplanation | None = None