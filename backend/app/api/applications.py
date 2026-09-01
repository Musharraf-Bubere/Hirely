from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.dependencies import require_candidate, require_recruiter
from app.db.session import get_db
from app.models.candidate import Candidate
from app.models.recruiter import Recruiter
from app.models.user import User
from app.models.application import Application
from app.models.job import Job
from app.schemas.application import (
    ApplicationResponse,
    ApplicationStatusUpdateRequest,
)
from app.services.application import (
    get_candidate_applications,
    get_recruiter_applications,
    update_application_status,
)


router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.get(
    "/me",
    response_model=list[ApplicationResponse],
)
def list_my_applications(
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.user_id == current_user.id)
        .first()
    )

    if not candidate:
        return []

    return get_candidate_applications(
        db=db,
        candidate=candidate,
    )


@router.get(
    "/recruiter",
    response_model=list[ApplicationResponse],
)
def list_recruiter_applications(
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db),
):
    recruiter = (
        db.query(Recruiter)
        .filter(Recruiter.user_id == current_user.id)
        .first()
    )

    if not recruiter:
        return []

    return get_recruiter_applications(
        db=db,
        recruiter_id=recruiter.id,
    )


@router.patch(
    "/{application_id}/status",
    response_model=ApplicationResponse,
)
def update_status(
    application_id: UUID,
    data: ApplicationStatusUpdateRequest,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db),
):
    recruiter = (
        db.query(Recruiter)
        .filter(
            Recruiter.user_id == current_user.id,
        )
        .first()
    )

    if not recruiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found",
        )

    application = (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .filter(
            Application.id == application_id,
            Job.recruiter_id == recruiter.id,
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return update_application_status(
        db=db,
        application=application,
        status=data.status,
    )