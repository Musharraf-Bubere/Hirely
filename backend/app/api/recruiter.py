from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.candidate_intelligence.schemas import (
    CandidateIntelligenceFilterRequest,
    CandidateIntelligenceResponse,
)
from app.ai.candidate_intelligence.service import (
    candidate_intelligence_service,
)
from app.ai.job_description_analyzer.schemas import (
    JobDescriptionAnalysisResponse,
)
from app.ai.job_description_analyzer.service import (
    job_description_analyzer_service,
)
from app.api.dependencies import require_recruiter
from app.db.session import get_db
from app.models.job import Job
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


@router.post(
    "/jobs/{job_id}/description-analysis",
    response_model=JobDescriptionAnalysisResponse,
)
def analyze_job_description(
    job_id: UUID,
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

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    if job.recruiter_id != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to analyze this job",
        )

    if not job.description or not job.description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty for analysis",
        )

    try:
        return job_description_analyzer_service.analyze_job_description(
            db=db,
            recruiter=recruiter,
            job=job,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Job Description Analyzer service is temporarily unavailable.",
        ) from exc


@router.post(
    "/jobs/{job_id}/candidate-intelligence",
    response_model=CandidateIntelligenceResponse,
)
def get_candidate_intelligence(
    job_id: UUID,
    filters: CandidateIntelligenceFilterRequest | None = None,
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

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    if job.recruiter_id != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view candidate intelligence for this job",
        )

    if not job.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target job is inactive",
        )

    try:
        return candidate_intelligence_service.get_candidate_intelligence(
            db=db,
            recruiter=recruiter,
            job=job,
            filters=filters,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Candidate Intelligence service is temporarily unavailable.",
        ) from exc