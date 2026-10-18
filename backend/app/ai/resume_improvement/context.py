from pydantic import BaseModel, Field

from app.ai.parsers.schemas import (
    Certification,
    Education,
    Project,
    ResumeData,
    WorkExperience,
)


class ResumeImprovementCandidateContext(BaseModel):
    """
    Candidate resume context sanitized of direct personal contact identifiers.
    Email, phone number, and physical street addresses are intentionally excluded
    to protect candidate privacy and avoid unnecessary PII transmission.
    """

    name: str | None = None
    headline: str | None = None
    bio: str | None = None
    location: str | None = None
    skills: list[str] = Field(default_factory=list)
    summary: str | None = None
    experience: list[WorkExperience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)


class ResumeImprovementJobContext(BaseModel):
    title: str
    description: str
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)


class ResumeImprovementDeterministicSignalsContext(BaseModel):
    ats_score: int
    required_skill_score: float
    preferred_skill_score: float
    semantic_relevance_score: float
    resume_completeness_score: float
    required_skills_matched: list[str] = Field(default_factory=list)
    required_skills_missing: list[str] = Field(default_factory=list)
    preferred_skills_matched: list[str] = Field(default_factory=list)
    preferred_skills_missing: list[str] = Field(default_factory=list)
    empty_or_missing_sections: list[str] = Field(default_factory=list)


class ResumeImprovementContext(BaseModel):
    candidate: ResumeImprovementCandidateContext
    job: ResumeImprovementJobContext
    deterministic_signals: ResumeImprovementDeterministicSignalsContext


class ResumeImprovementContextBuilder:
    def build(
        self,
        *,
        first_name: str | None,
        last_name: str | None,
        headline: str | None,
        bio: str | None,
        location: str | None,
        candidate_skills: list[str],
        resume_data: ResumeData,
        job_title: str,
        job_description: str,
        job_location: str | None,
        employment_type: str | None,
        experience_level: str | None,
        required_skills: list[str],
        preferred_skills: list[str],
        deterministic_signals: ResumeImprovementDeterministicSignalsContext,
    ) -> ResumeImprovementContext:
        full_name = f"{first_name or ''} {last_name or ''}".strip() or resume_data.name

        combined_skills = list(
            {
                skill.strip()
                for skill in (candidate_skills + resume_data.skills)
                if skill and skill.strip()
            }
        )
        combined_skills.sort()

        normalized_required_skills = sorted(
            {
                skill.strip()
                for skill in required_skills
                if skill and skill.strip()
            }
        )

        normalized_preferred_skills = sorted(
            {
                skill.strip()
                for skill in preferred_skills
                if skill and skill.strip()
            }
        )

        effective_headline = (
            headline
            or resume_data.headline
            or None
        )
        effective_location = (
            location
            or resume_data.location
            or None
        )

        return ResumeImprovementContext(
            candidate=ResumeImprovementCandidateContext(
                name=full_name or None,
                headline=effective_headline,
                bio=bio or None,
                location=effective_location,
                skills=combined_skills,
                summary=resume_data.summary or None,
                experience=resume_data.experience,
                projects=resume_data.projects,
                education=resume_data.education,
                certifications=resume_data.certifications,
            ),
            job=ResumeImprovementJobContext(
                title=job_title,
                description=job_description,
                location=job_location,
                employment_type=employment_type,
                experience_level=experience_level,
                required_skills=normalized_required_skills,
                preferred_skills=normalized_preferred_skills,
            ),
            deterministic_signals=deterministic_signals,
        )


resume_improvement_context_builder = ResumeImprovementContextBuilder()
