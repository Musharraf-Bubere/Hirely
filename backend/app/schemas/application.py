from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.application import ApplicationStatus


class ApplicationResponse(BaseModel):
    id: UUID
    candidate_id: UUID
    job_id: UUID
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }

class ApplicationStatusUpdateRequest(BaseModel):
    status: ApplicationStatus