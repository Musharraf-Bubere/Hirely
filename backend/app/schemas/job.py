from uuid import UUID

from pydantic import BaseModel, Field


class JobCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10, max_length=15000)
    location: str | None = None
    employment_type: str
    experience_level: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None


class JobResponse(BaseModel):
    id: UUID
    recruiter_id: UUID
    title: str
    description: str
    location: str | None
    employment_type: str
    experience_level: str | None
    salary_min: int | None
    salary_max: int | None
    is_active: bool

    model_config = {
        "from_attributes": True,
    }