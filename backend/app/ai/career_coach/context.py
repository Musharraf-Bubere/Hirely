from pydantic import BaseModel, Field

from app.ai.parsers.schemas import ResumeData


class CareerCoachJobContext(BaseModel):
    """
    AI-safe representation of a job associated with the candidate.
    """

    title: str
    description: str
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None


class CareerCoachApplicationContext(BaseModel):
    """
    AI-safe representation of a candidate's application.
    """

    status: str
    job: CareerCoachJobContext


class CareerCoachCandidateContext(BaseModel):
    """
    AI-safe candidate context used by the Career Coach.

    This intentionally excludes sensitive/internal fields such as:
    - user ID
    - candidate ID
    - email
    - phone
    - resume file path
    - authentication information
    """

    name: str | None = None
    headline: str | None = None
    bio: str | None = None
    location: str | None = None

    skills: list[str] = Field(default_factory=list)

    resume: ResumeData | None = None

    applications: list[CareerCoachApplicationContext] = Field(
        default_factory=list
    )


class CareerCoachContextBuilder:
    """
    Builds the AI-safe context required by the Career Coach.
    """

    def build(
        self,
        *,
        first_name: str,
        last_name: str,
        headline: str | None,
        bio: str | None,
        location: str | None,
        skills: list[str],
        resume_data: ResumeData | None = None,
        applications: list[CareerCoachApplicationContext] | None = None,
    ) -> CareerCoachCandidateContext:
        """
        Build a candidate context from candidate profile data,
        skills, optional resume data, and optional application data.
        """

        full_name = f"{first_name} {last_name}".strip()

        return CareerCoachCandidateContext(
            name=full_name or None,
            headline=headline,
            bio=bio,
            location=location,
            skills=sorted(
                {
                    skill.strip()
                    for skill in skills
                    if skill and skill.strip()
                }
            ),
            resume=resume_data,
            applications=applications or [],
        )


career_coach_context_builder = CareerCoachContextBuilder()