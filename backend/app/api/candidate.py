from fastapi import APIRouter, Depends

from app.api.dependencies import require_candidate
from app.models.user import User


router = APIRouter(
    prefix="/candidate",
    tags=["Candidate"],
)


@router.get("/profile")
def get_candidate_profile(
    current_user: User = Depends(require_candidate),
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
    }