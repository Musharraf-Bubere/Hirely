from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class CandidateProfileResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool

    first_name: str
    last_name: str
    headline: str | None
    bio: str | None
    location: str | None