from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_candidate
from app.db.session import get_db
from app.models.candidate import Candidate
from app.models.user import User
from app.schemas.candidate import (
    CandidateProfileCreate,
    CandidateProfileResponse,
    CandidateProfileUpdate,
)
from app.services.candidate import (
    create_candidate_profile,
    update_candidate_profile,
)


router = APIRouter(
    prefix="/candidate",
    tags=["Candidate"],
)


@router.post(
    "/profile",
    response_model=CandidateProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    data: CandidateProfileCreate,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    try:
        candidate = create_candidate_profile(
            db=db,
            user=current_user,
            data=data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )

    return {
        "id": candidate.id,
        "email": current_user.email,
        "first_name": candidate.first_name,
        "last_name": candidate.last_name,
        "headline": candidate.headline,
        "bio": candidate.bio,
        "location": candidate.location,
    }


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
        "id": candidate.id,
        "email": current_user.email,
        "first_name": candidate.first_name,
        "last_name": candidate.last_name,
        "headline": candidate.headline,
        "bio": candidate.bio,
        "location": candidate.location,
    }


@router.patch(
    "/profile",
    response_model=CandidateProfileResponse,
)
def update_profile(
    data: CandidateProfileUpdate,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    try:
        candidate = update_candidate_profile(
            db=db,
            user=current_user,
            data=data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return {
        "id": candidate.id,
        "email": current_user.email,
        "first_name": candidate.first_name,
        "last_name": candidate.last_name,
        "headline": candidate.headline,
        "bio": candidate.bio,
        "location": candidate.location,
    }