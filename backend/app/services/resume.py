from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.resume import Resume
from app.ai.parsers.resume_parser import ResumeParserService

def create_resume(
    db: Session,
    candidate: Candidate,
    original_filename: str,
    file_path: str,
) -> Resume:
    resume = Resume(
        candidate_id=candidate.id,
        original_filename=original_filename,
        file_path=file_path,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume

def parse_resume(
    db: Session,
    resume: Resume,
    parser_service: ResumeParserService,
) -> Resume:
    resume.parsing_status = "PROCESSING"
    db.commit()
    db.refresh(resume)

    try:
        resume_data = parser_service.parse_file(
            resume.file_path,
        )

        resume.parsed_data = resume_data.model_dump()
        resume.parsing_status = "COMPLETED"

        db.commit()
        db.refresh(resume)

        return resume

    except Exception:
        resume.parsing_status = "FAILED"

        db.commit()
        db.refresh(resume)

        raise

def activate_resume(
    db: Session,
    candidate: Candidate,
    resume: Resume,
) -> Resume:
    if resume.candidate_id != candidate.id:
        raise ValueError("Resume does not belong to candidate")

    (
        db.query(Resume)
        .filter(
            Resume.candidate_id == candidate.id,
            Resume.is_active.is_(True),
            Resume.id != resume.id,
        )
        .update(
            {
                Resume.is_active: False,
            },
            synchronize_session=False,
        )
    )

    resume.is_active = True

    db.commit()
    db.refresh(resume)

    return resume

def get_active_resume(
    db: Session,
    candidate: Candidate,
) -> Resume | None:
    return (
        db.query(Resume)
        .filter(
            Resume.candidate_id == candidate.id,
            Resume.is_active.is_(True),
        )
        .first()
    )

def get_resumes(
    db: Session,
    candidate: Candidate,
) -> list[Resume]:
    return (
        db.query(Resume)
        .filter(
            Resume.candidate_id == candidate.id,
        )
        .order_by(
            Resume.created_at.desc(),
        )
        .all()
    )