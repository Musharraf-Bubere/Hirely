from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_recruiter
from app.db.session import get_db
from app.models.recruiter import Recruiter
from app.models.user import User
from app.schemas.job import JobResponse
from app.schemas.recruiter import RecruiterProfileResponse
from app.services.job import get_recruiter_jobs


router = APIRouter(
    prefix="/recruiter",
    tags=["Recruiter"],
)


@router.get(
    "/profile",
    response_model=RecruiterProfileResponse,
)
def get_recruiter_profile(
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db),
):
    recruiter = (
        db.query(Recruiter)
        .filter(Recruiter.user_id == current_user.id)
        .first()
    )

    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found",
        )

    company = recruiter.company

    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "first_name": recruiter.first_name,
        "last_name": recruiter.last_name,
        "job_title": recruiter.job_title,
        "location": recruiter.location,
        "company": company,
    }


@router.get(
    "/jobs",
    response_model=list[JobResponse],
)
def get_my_jobs(
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db),
):
    recruiter = (
        db.query(Recruiter)
        .filter(Recruiter.user_id == current_user.id)
        .first()
    )

    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found",
        )

    return get_recruiter_jobs(
        db=db,
        recruiter=recruiter,
    )