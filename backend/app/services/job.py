from uuid import UUID

from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.recruiter import Recruiter
from app.schemas.job import JobCreateRequest


def create_job(
    db: Session,
    recruiter: Recruiter,
    data: JobCreateRequest,
) -> Job:
    job = Job(
        recruiter_id=recruiter.id,
        title=data.title,
        description=data.description,
        location=data.location,
        employment_type=data.employment_type,
        experience_level=data.experience_level,
        salary_min=data.salary_min,
        salary_max=data.salary_max,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_active_jobs(
        db: Session,
) -> list[Job]:
    return (
        db.query(Job)
        .filter(Job.is_active.is_(True))
        .order_by(Job.created_at.desc())
        .all()
    )


def get_active_job(
    db: Session,
    job_id: UUID,
) -> Job | None:
    return (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.is_active.is_(True),
        )
        .first()
    )