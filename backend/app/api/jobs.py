from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_candidate
from app.api.dependencies import require_recruiter
from app.db.session import get_db
from app.models.candidate import Candidate
from app.models.recruiter import Recruiter
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreateRequest, JobResponse
from app.services.job import create_job, get_active_jobs, get_active_job
from app.schemas.application import ApplicationResponse
from app.services.application import create_application


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job_endpoint(
    data: JobCreateRequest,
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

    return create_job(
        db=db,
        recruiter=recruiter,
        data=data,
    )

@router.get(
    "",
    response_model=list[JobResponse],
)
def list_jobs(
    db: Session = Depends(get_db),
):
    return get_active_jobs(db)

@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    job = get_active_job(
        db=db,
        job_id=job_id,
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job

@router.post(
    "/{job_id}/apply",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def apply_to_job(
    job_id: UUID,
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

    job = (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.is_active.is_(True),
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    try:
        application = create_application(
            db=db,
            candidate=candidate,
            job=job,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return application