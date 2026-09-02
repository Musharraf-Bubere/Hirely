from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_recruiter
from app.db.session import get_db
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.models.recruiter import Recruiter
from app.models.user import User
from app.schemas.skill import JobSkillCreateRequest
from app.services.job_skill import add_job_skill
from app.services.skill import get_or_create_skill


router = APIRouter(
    prefix="/jobs/{job_id}/skills",
    tags=["Job Skills"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def add_skill_to_job(
    job_id: UUID,
    data: JobSkillCreateRequest,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db),
):
    # ---------------------------------------------------------
    # Find recruiter profile
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Find job
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Verify job ownership
    # ---------------------------------------------------------
    if job.recruiter_id != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage this job",
        )

    # ---------------------------------------------------------
    # Find existing skill or create a new one
    # ---------------------------------------------------------
    skill = get_or_create_skill(
        db=db,
        data=data,
    )

    # ---------------------------------------------------------
    # Create Job ↔ Skill association
    # ---------------------------------------------------------
    try:
        job_skill = add_job_skill(
            db=db,
            job=job,
            skill=skill,
            is_required=data.is_required,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return {
        "skill_id": job_skill.skill_id,
        "name": skill.name,
        "is_required": job_skill.is_required,
    }


@router.get(
    "",
)
def get_job_skills(
    job_id: UUID,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db),
):
    # ---------------------------------------------------------
    # Find recruiter profile
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Find job
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Verify job ownership
    # ---------------------------------------------------------
    if job.recruiter_id != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage this job",
        )

    # ---------------------------------------------------------
    # Get job skills
    # ---------------------------------------------------------
    job_skills = (
        db.query(JobSkill)
        .filter(JobSkill.job_id == job.id)
        .all()
    )

    return [
        {
            "skill_id": job_skill.skill_id,
            "name": job_skill.skill.name,
            "is_required": job_skill.is_required,
        }
        for job_skill in job_skills
    ]


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_skill_from_job(
    job_id: UUID,
    skill_id: UUID,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db),
):
    # ---------------------------------------------------------
    # Find recruiter profile
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Find job
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Verify job ownership
    # ---------------------------------------------------------
    if job.recruiter_id != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to manage this job",
        )

    # ---------------------------------------------------------
    # Find job-skill association
    # ---------------------------------------------------------
    job_skill = (
        db.query(JobSkill)
        .filter(
            JobSkill.job_id == job.id,
            JobSkill.skill_id == skill_id,
        )
        .first()
    )

    if not job_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found for job",
        )

    # ---------------------------------------------------------
    # Remove association
    # ---------------------------------------------------------
    db.delete(job_skill)
    db.commit()

    return None