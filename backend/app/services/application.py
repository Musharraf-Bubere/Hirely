from sqlalchemy.orm import Session

from app.models.application import Application, ApplicationStatus
from app.models.candidate import Candidate
from app.models.job import Job


def create_application(
    db: Session,
    candidate: Candidate,
    job: Job,
) -> Application:
    existing_application = (
        db.query(Application)
        .filter(
            Application.candidate_id == candidate.id,
            Application.job_id == job.id,
        )
        .first()
    )

    if existing_application:
        raise ValueError("You have already applied to this job")

    application = Application(
        candidate_id=candidate.id,
        job_id=job.id,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_candidate_applications(
    db: Session,
    candidate: Candidate,
) -> list[Application]:
    return (
        db.query(Application)
        .filter(
            Application.candidate_id == candidate.id,
        )
        .order_by(Application.created_at.desc())
        .all()
    )


def get_recruiter_applications(
    db: Session,
    recruiter_id,
) -> list[Application]:
    return (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .filter(
            Job.recruiter_id == recruiter_id,
        )
        .order_by(Application.created_at.desc())
        .all()
    )


def update_application_status(
    db: Session,
    application: Application,
    status: ApplicationStatus,
) -> Application:
    application.status = status

    db.commit()
    db.refresh(application)

    return application