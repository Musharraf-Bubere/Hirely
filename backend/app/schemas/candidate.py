from uuid import UUID

from pydantic import BaseModel, Field


class CandidateProfileCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    headline: str | None = Field(default=None, max_length=255)
    bio: str | None = None
    location: str | None = Field(default=None, max_length=255)


class CandidateProfileUpdate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    headline: str | None = Field(default=None, max_length=255)
    bio: str | None = None
    location: str | None = Field(default=None, max_length=255)


class CandidateProfileResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    headline: str | None = None
    bio: str | None = None
    location: str | None = None

    model_config = {
        "from_attributes": True
    }