from uuid import UUID

from pydantic import BaseModel, Field


class ATSAnalysisRequest(BaseModel):
    job_id: UUID


class ATSScoreBreakdown(BaseModel):
    required_skill_score: float = Field(
        ge=0.0,
        le=1.0,
    )
    preferred_skill_score: float = Field(
        ge=0.0,
        le=1.0,
    )
    semantic_relevance_score: float = Field(
        ge=0.0,
        le=1.0,
    )
    resume_completeness_score: float = Field(
        ge=0.0,
        le=1.0,
    )


class ATSAnalysisResult(BaseModel):
    ats_score: int = Field(
        ge=0,
        le=100,
    )

    score_breakdown: ATSScoreBreakdown

    required_skills_matched: list[str] = Field(
        default_factory=list,
    )

    required_skills_missing: list[str] = Field(
        default_factory=list,
    )

    preferred_skills_matched: list[str] = Field(
        default_factory=list,
    )

    preferred_skills_missing: list[str] = Field(
        default_factory=list,
    )

    strengths: list[str] = Field(
        default_factory=list,
    )

    improvement_areas: list[str] = Field(
        default_factory=list,
    )

    suggestions: list[str] = Field(
        default_factory=list,
    )

    summary: str


class ATSAnalysisResponse(BaseModel):
    job_id: UUID
    ats_analysis: ATSAnalysisResult