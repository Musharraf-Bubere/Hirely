from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    id: UUID
    filename: str
    content_type: str | None = None
    parsing_status: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ResumeResponse(BaseModel):
    id: UUID
    original_filename: str
    parsing_status: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
