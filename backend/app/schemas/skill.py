from uuid import UUID

from pydantic import BaseModel


class SkillCreateRequest(BaseModel):
    name: str


class JobSkillCreateRequest(BaseModel):
    name: str
    is_required: bool = True


class SkillResponse(BaseModel):
    id: UUID
    name: str

    model_config = {
        "from_attributes": True,
    }