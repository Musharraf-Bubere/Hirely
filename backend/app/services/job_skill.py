from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.job_skill import JobSkill
from app.models.skill import Skill


def add_job_skill(
    db: Session,
    job: Job,
    skill: Skill,
    is_required: bool,
) -> JobSkill:
    existing = (
        db.query(JobSkill)
        .filter(
            JobSkill.job_id == job.id,
            JobSkill.skill_id == skill.id,
        )
        .first()
    )

    if existing:
        raise ValueError("Skill already added to job")

    job_skill = JobSkill(
        job_id=job.id,
        skill_id=skill.id,
        is_required=is_required,
    )

    db.add(job_skill)
    db.commit()
    db.refresh(job_skill)

    return job_skill