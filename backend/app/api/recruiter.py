from fastapi import APIRouter, Depends

from app.api.dependencies import require_recruiter
from app.models.user import User


router = APIRouter(
    prefix="/recruiter",
    tags=["Recruiter"],
)


@router.get("/profile")
def get_recruiter_profile(
    current_user: User = Depends(require_recruiter),
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }