from pydantic import BaseModel, Field

from app.ai.parsers.schemas import ResumeData


class CoverLetterCandidateContext(BaseModel):
    """
    AI-safe candidate context used for cover letter generation.

    Sensitive/internal fields such as user ID, candidate ID,
    email, phone, resume file path, and authentication data
    are intentionally excluded.
    """

    name: str | None = None
    headline: str | None = None
    bio: str | None = None
    location: str | None = None

    skills: list[str] = Field(default_factory=list)

    resume: ResumeData | None = None


class CoverLetterJobContext(BaseModel):
    """
    AI-safe representation of the target job.
    """

    title: str
    description: str
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None

    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)


class CoverLetterContext(BaseModel):
    """
    Complete AI-safe context used to generate a
    job-specific cover letter.
    """

    candidate: CoverLetterCandidateContext
    job: CoverLetterJobContext


class CoverLetterContextBuilder:
    """
    Builds the AI-safe context required for cover letter generation.
    """

    def build(
        self,
        *,
        first_name: str,
        last_name: str,
        headline: str | None,
        bio: str | None,
        location: str | None,
        candidate_skills: list[str],
        resume_data: ResumeData | None,
        job_title: str,
        job_description: str,
        job_location: str | None,
        employment_type: str | None,
        experience_level: str | None,
        required_skills: list[str],
        preferred_skills: list[str],
    ) -> CoverLetterContext:
        """
        Build a complete candidate + job context.

        Skill names are normalized for consistent AI input by
        trimming whitespace, removing empty values, and sorting
        unique values.
        """

        full_name = f"{first_name} {last_name}".strip()

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

        return CoverLetterContext(
            candidate=CoverLetterCandidateContext(
                name=full_name or None,
                headline=headline,
                bio=bio,
                location=location,
                skills=normalized_candidate_skills,
                resume=resume_data,
            ),
            job=CoverLetterJobContext(
                title=job_title,
                description=job_description,
                location=job_location,
                employment_type=employment_type,
                experience_level=experience_level,
                required_skills=normalized_required_skills,
                preferred_skills=normalized_preferred_skills,
            ),
        )


cover_letter_context_builder = CoverLetterContextBuilder()