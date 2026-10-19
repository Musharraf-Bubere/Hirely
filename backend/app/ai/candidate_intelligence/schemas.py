from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.ai.matching.explanation import MatchExplanation


class CandidateExperienceItem(BaseModel):
    job_title: str | None = None
    company: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None


class CandidateEducationItem(BaseModel):
    degree: str | None = None
    institution: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class CandidateProfileSummary(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    full_name: str
    headline: str | None = None
    location: str | None = None
    bio: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience: list[CandidateExperienceItem] = Field(default_factory=list)
    education: list[CandidateEducationItem] = Field(default_factory=list)


class CandidateApplicationInfo(BaseModel):
    application_id: UUID | None = None
    status: str | None = None
    created_at: datetime | None = None


class CandidateIntelligenceItem(BaseModel):
    rank: int
    candidate: CandidateProfileSummary
    application: CandidateApplicationInfo | None = None
    overall_score: float = Field(ge=0.0, le=1.0)
    required_skill_score: float = Field(ge=0.0, le=1.0)
    preferred_skill_score: float | None = Field(default=None, ge=0.0, le=1.0)
    semantic_similarity: float = Field(ge=0.0, le=1.0)
    required_matched: list[str] = Field(default_factory=list)
    required_missing: list[str] = Field(default_factory=list)
    preferred_matched: list[str] = Field(default_factory=list)
    preferred_missing: list[str] = Field(default_factory=list)
    explanation: MatchExplanation | None = None


class CandidateIntelligenceFilterRequest(BaseModel):
    query: str | None = Field(
        default=None,
        max_length=200,
        description="Keyword search query across candidate name, headline, bio, and skills.",
    )
    min_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Minimum overall match score filter (0.0 to 1.0).",
    )
    skill: str | None = Field(
        default=None,
        description="Filter for candidates possessing this specific skill.",
    )
    application_status: str | None = Field(
        default=None,
        description="Filter by application status: 'applied', 'shortlisted', 'interview', 'hired', 'rejected', 'not_applied', or 'all'.",
    )
    sort_by: str = Field(
        default="overall_score",
        description="Sort by 'overall_score', 'required_skills', 'preferred_skills', 'semantic_similarity', 'name', or 'rank'.",
    )
    sort_order: str = Field(
        default="desc",
        description="Sort order: 'desc' or 'asc'.",
    )
    include_explanations: bool = Field(
        default=True,
        description="Whether to include AI match explanations for top-ranked candidates.",
    )
    explanation_limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of top candidates to generate AI explanations for.",
    )


class CandidateIntelligenceResponse(BaseModel):
    job_id: UUID
    job_title: str
    total_candidates: int
    matched_count: int
    results: list[CandidateIntelligenceItem]
    available_skills: list[str] = Field(default_factory=list)
    disclaimer: str = Field(
        default=(
            "Match scores and rankings are calculated deterministically by Hirely's matching engine based on verified skills and semantic relevance. "
            "AI explanations and recommendations are assistive and advisory."
        ),
        description="Advisory disclaimer.",
    )
