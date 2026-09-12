from uuid import UUID

from pydantic import BaseModel, Field


class CoverLetterRequest(BaseModel):
    job_id: UUID = Field(
        ...,
        description="ID of the job for which the cover letter should be generated.",
    )


class CoverLetterResponse(BaseModel):
    cover_letter: str