from pydantic import BaseModel, Field

from app.ai.parsers.schemas import ResumeData


class ATSCandidateContext(BaseModel):
    name: str | None = None
    headline: str | None = None
    bio: str | None = None
    location: str | None = None
    skills: list[str] = Field(default_factory=list)
    resume: ResumeData


class ATSJobContext(BaseModel):
    title: str
    description: str
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)


class ATSContext(BaseModel):
    candidate: ATSCandidateContext
    job: ATSJobContext


class ATSContextBuilder:
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
    ) -> ATSContext:
        full_name = f"{first_name or ''} {last_name or ''}".strip()

        normalized_candidate_skills = sorted(
            {
                skill.strip()
                for skill in candidate_skills
                if skill and skill.strip()
            }
        )

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

        return ATSContext(
            candidate=ATSCandidateContext(
                name=full_name or None,
                headline=headline,
                bio=bio,
                location=location,
                skills=normalized_candidate_skills,
                resume=resume_data,
            ),
            job=ATSJobContext(
                title=job_title,
                description=job_description,
                location=job_location,
                employment_type=employment_type,
                experience_level=experience_level,
                required_skills=normalized_required_skills,
                preferred_skills=normalized_preferred_skills,
            ),
        )


ats_context_builder = ATSContextBuilder()