from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: UserRole

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool

    model_config = {
        "from_attributes": True,
    }

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"