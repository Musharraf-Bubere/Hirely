from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_candidate
from app.db.session import get_db
from app.models.candidate import Candidate
from app.models.user import User
from app.schemas.candidate import CandidateProfileResponse


router = APIRouter(
    prefix="/candidate",
    tags=["Candidate"],
)


@router.get(
    "/profile",
    response_model=CandidateProfileResponse,
)
def get_candidate_profile(
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.user_id == current_user.id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate profile not found",
        )

    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "first_name": candidate.first_name,
        "last_name": candidate.last_name,
        "headline": candidate.headline,
        "bio": candidate.bio,
        "location": candidate.location,
    }