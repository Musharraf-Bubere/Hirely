from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.career_coach.schemas import (
    CareerCoachRequest,
    CareerCoachResponse,
)
from app.ai.career_coach.service import career_coach_service
from app.ai.cover_letter.schemas import (
    CoverLetterRequest,
    CoverLetterResponse,
)
from app.ai.cover_letter.service import cover_letter_service
from app.api.dependencies import (
    get_current_candidate,
    require_candidate,
)
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
from app.services.job import get_active_job


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


@router.post(
    "/career-coach",
    response_model=CareerCoachResponse,
)
def career_coach(
    data: CareerCoachRequest,
    candidate: Candidate = Depends(get_current_candidate),
    db: Session = Depends(get_db),
):
    try:
        return career_coach_service.generate_response(
            db=db,
            candidate=candidate,
            request=data,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Career Coach service is temporarily unavailable.",
        ) from exc


@router.post(
    "/cover-letter",
    response_model=CoverLetterResponse,
)
def generate_cover_letter(
    data: CoverLetterRequest,
    candidate: Candidate = Depends(get_current_candidate),
    db: Session = Depends(get_db),
):
    job = get_active_job(
        db=db,
        job_id=data.job_id,
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    try:
        return cover_letter_service.generate_cover_letter(
            db=db,
            candidate=candidate,
            job=job,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Cover Letter service is temporarily unavailable.",
        ) from exc