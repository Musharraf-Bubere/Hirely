import logging
from uuid import UUID

from app.models.resume import Resume

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_candidate
from app.core.rate_limit import check_ai_rate_limit
from app.ai.services.candidate_preparation_service import candidate_embedding_cache
from app.db.session import get_db
from app.storage.file_validation import validate_resume_file
from app.storage.storage_service import storage_service
from app.ai.parsers.resume_parser import ResumeParserService
from app.services.resume import (
    activate_resume,
    create_resume,
    delete_resume,
    get_resumes,
    parse_resume,
)
from app.schemas.resume import ResumeResponse, ResumeUploadResponse
from app.services.resume_skill import sync_resume_skills_to_candidate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post(
    "",
    response_model=ResumeUploadResponse,
)
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
        "id": resume_record.id,
        "filename": resume.filename,
        "content_type": resume.content_type,
        "parsing_status": resume_record.parsing_status,
        "is_active": resume_record.is_active,
        "created_at": resume_record.created_at,
    }


@router.get(
    "",
    response_model=list[ResumeResponse],
)
def list_resumes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    candidate=Depends(get_current_candidate),
    db: Session = Depends(get_db),
):
    return get_resumes(
        db=db,
        candidate=candidate,
        skip=skip,
        limit=limit,
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
        activated = activate_resume(
            db=db,
            candidate=candidate,
            resume=resume,
        )
        candidate_embedding_cache.invalidate(candidate.id)
        return activated
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
    _rate_limit=Depends(check_ai_rate_limit),
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

        candidate_embedding_cache.invalidate(candidate.id)

        return resume

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Resume parsing failed unexpectedly for candidate %s: %s", candidate.id, type(exc).__name__)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Resume parsing failed due to an internal service error. Please try again.",
        ) from exc


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_200_OK,
)
def delete_resume_endpoint(
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

    try:
        delete_resume(
            db=db,
            candidate=candidate,
            resume=resume,
        )
        candidate_embedding_cache.invalidate(candidate.id)
        return {"status": "success", "message": "Resume deleted successfully"}
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
