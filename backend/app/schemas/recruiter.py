from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class CompanyResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    website: str | None
    industry: str | None
    location: str | None


class RecruiterProfileResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool

    first_name: str
    last_name: str
    job_title: str | None
    location: str | None

    company: CompanyResponse | None