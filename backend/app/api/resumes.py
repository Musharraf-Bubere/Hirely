from uuid import UUID

from app.models.resume import Resume

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_candidate
from app.db.session import get_db
from app.storage.file_validation import validate_resume_file
from app.storage.storage_service import storage_service
from app.ai.parsers.resume_parser import ResumeParserService
from app.services.resume import (
    activate_resume,
    create_resume,
    get_resumes,
    parse_resume,
)
from app.schemas.resume import ResumeResponse
from app.services.resume_skill import sync_resume_skills_to_candidate

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("")
def upload_resume(
    resume: UploadFile = File(...),
    candidate=Depends(get_current_candidate),
    db: Session = Depends(get_db),
):
    try:
        validate_resume_file(resume)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    file_path = storage_service.save_resume(resume)

    resume_record = create_resume(
        db=db,
        candidate=candidate,
        original_filename=resume.filename,
        file_path=file_path,
    )

    return {
        "filename": resume.filename,
        "content_type": resume.content_type,
        "file_path": file_path,
    }


@router.get(
    "",
    response_model=list[ResumeResponse],
)
def list_resumes(
    candidate=Depends(get_current_candidate),
    db: Session = Depends(get_db),
):
    return get_resumes(
        db=db,
        candidate=candidate,
    )

@router.patch(
    "/{resume_id}/activate",
    response_model=ResumeResponse,
)
def activate_resume_endpoint(
    resume_id: UUID,
    candidate=Depends(get_current_candidate),
    db: Session = Depends(get_db),
):
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id)
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    try:
        return activate_resume(
            db=db,
            candidate=candidate,
            resume=resume,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

@router.post(
    "/{resume_id}/parse",
    response_model=ResumeResponse,
)
def parse_resume_endpoint(
    resume_id: UUID,
    candidate=Depends(get_current_candidate),
    db: Session = Depends(get_db),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.candidate_id == candidate.id,
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    parser_service = ResumeParserService()

    try:
        resume = parse_resume(
            db=db,
            resume=resume,
            parser_service=parser_service,
        )

        sync_resume_skills_to_candidate(
            db=db,
            candidate=candidate,
            resume=resume,
        )

        return resume

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume parsing failed: {str(exc)}",
        ) from exc