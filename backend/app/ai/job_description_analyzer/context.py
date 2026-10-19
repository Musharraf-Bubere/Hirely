from uuid import UUID

from pydantic import BaseModel, Field

from app.models.job import Job


class JobDescriptionContext(BaseModel):
    job_id: UUID
    title: str
    description: str
    location: str | None = None
    employment_type: str
    experience_level: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    is_active: bool = True
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)


def _normalize_skills(skills: list[str] | None) -> list[str]:
    if not skills:
        return []
    seen = set()
    result = []
    for raw in skills:
        if not raw:
            continue
        cleaned = raw.strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)
    return sorted(result)


class JobDescriptionContextBuilder:
    """
    Builds structured, normalized context from an existing recruiter job.
    """

    def build(
        self,
        *,
        job: Job,
        required_skills: list[str] | None = None,
        preferred_skills: list[str] | None = None,
    ) -> JobDescriptionContext:
        if not job.description or not job.description.strip():
            raise ValueError("Job description cannot be empty for analysis.")

        normalized_required = _normalize_skills(required_skills)
        normalized_preferred = _normalize_skills(preferred_skills)

        return JobDescriptionContext(
            job_id=job.id,
            title=job.title.strip(),
            description=job.description.strip(),
            location=job.location.strip() if job.location else None,
            employment_type=job.employment_type.strip() if job.employment_type else "Not specified",
            experience_level=job.experience_level.strip() if job.experience_level else None,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            is_active=True if job.is_active is None else bool(job.is_active),
            required_skills=normalized_required,
            preferred_skills=normalized_preferred,
        )


job_description_context_builder = JobDescriptionContextBuilder()
