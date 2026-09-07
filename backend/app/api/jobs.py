from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    require_candidate,
    require_recruiter,
)

from app.ai.services.recruiter_matching_service import (
    recruiter_matching_service,
)

from app.db.session import get_db

from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User

from app.schemas.application import ApplicationResponse
from app.schemas.job import JobCreateRequest, JobResponse

from app.services.application import create_application

from app.services.job import (
    create_job,
    get_active_job,
    get_active_jobs,
)


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


# ---------------------------------------------------------
# Create Job
# ---------------------------------------------------------

@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_job(
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

    try:
        return create_job(
            db=db,
            recruiter=recruiter,
            data=data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# ---------------------------------------------------------
# List Active Jobs
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[JobResponse],
)
def list_active_jobs(
    db: Session = Depends(get_db),
):
    return get_active_jobs(db=db)


# ---------------------------------------------------------
# Get Active Job
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Apply to Job
# ---------------------------------------------------------

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

    job = get_active_job(
        db=db,
        job_id=job_id,
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    try:
        return create_application(
            db=db,
            candidate=candidate,
            job=job,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Candidate → Job Matching
# ---------------------------------------------------------

@router.post(
    "/{job_id}/match",
)
def match_candidate_to_job(
    job_id: UUID,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # 1. Get candidate profile
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # 2. Get active resume
    # -----------------------------------------------------

    from app.services.resume import get_active_resume

    resume = get_active_resume(
        db=db,
        candidate=candidate,
    )

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active resume not found",
        )

    # -----------------------------------------------------
    # 3. Resume must be parsed
    # -----------------------------------------------------

    if resume.parsing_status != "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Active resume has not been parsed",
        )

    if not resume.parsed_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Active resume has no parsed data",
        )

    # -----------------------------------------------------
    # 4. Validate resume data
    # -----------------------------------------------------

    from app.ai.parsers.schemas import ResumeData

    try:
        resume_data = ResumeData.model_validate(
            resume.parsed_data
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parsed resume data",
        )

    # -----------------------------------------------------
    # 5. Get active job
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # 6. Candidate and job skills
    # -----------------------------------------------------

    from app.services.candidate_skill import get_candidate_skills
    from app.services.job_skill import get_job_skills

    candidate_skills = get_candidate_skills(
        db=db,
        candidate=candidate,
    )

    required_skills, preferred_skills = get_job_skills(
        db=db,
        job=job,
    )

    # -----------------------------------------------------
    # 7. Prepare candidate and job
    # -----------------------------------------------------

    from app.ai.embeddings.service import embedding_service
    from app.ai.matching.engine import matching_engine
    from app.ai.representations.candidate import (
        candidate_representation_builder,
    )
    from app.ai.representations.job import (
        job_representation_builder,
    )
    from app.ai.services.candidate_preparation_service import (
        CandidatePreparationInput,
        CandidatePreparationService,
    )
    from app.ai.services.job_preparation_service import (
        JobPreparationInput,
        JobPreparationService,
    )
    from app.ai.services.matching_input_assembler import (
        MatchingInputAssembly,
        MatchingInputAssembler,
    )
    from app.ai.services.match_explanation_service import (
        match_explanation_service,
    )
    from app.ai.services.matching_orchestrator import (
        MatchingOrchestrator,
    )
    from app.ai.services.matching_service import (
        matching_service,
    )

    candidate_preparation_service = CandidatePreparationService(
        representation_builder=candidate_representation_builder,
        embedding_service=embedding_service,
    )

    job_preparation_service = JobPreparationService(
        representation_builder=job_representation_builder,
        embedding_service=embedding_service,
    )

    candidate_preparation = candidate_preparation_service.prepare(
        CandidatePreparationInput(
            candidate_id=candidate.id,
            resume_data=resume_data,
        )
    )

    job_preparation = job_preparation_service.prepare(
        JobPreparationInput(
            job_id=job.id,
            title=job.title,
            description=job.description,
            location=job.location,
            employment_type=job.employment_type,
            experience_level=job.experience_level,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
        )
    )

    # -----------------------------------------------------
    # 8. Assemble matching input
    # -----------------------------------------------------

    matching_input_assembler = MatchingInputAssembler()

    matching_input = matching_input_assembler.assemble(
        MatchingInputAssembly(
            candidate_preparation=candidate_preparation,
            candidate_skills=candidate_skills,
            job_preparation=job_preparation,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
        )
    )

    # -----------------------------------------------------
    # 9. Run matching engine
    # -----------------------------------------------------

    matching_orchestrator = MatchingOrchestrator(
        matching_engine=matching_engine,
        matching_service=matching_service,
        match_explanation_service=match_explanation_service,
    )

    result = matching_orchestrator.match(
        matching_input
    )

    return result


# ---------------------------------------------------------
# Recruiter → Candidate Matching
# ---------------------------------------------------------

@router.post(
    "/{job_id}/candidates/match",
)
def match_candidates_to_job(
    job_id: UUID,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # 1. Get recruiter profile
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # 2. Get active job
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # 3. Verify job ownership
    # -----------------------------------------------------

    if job.recruiter_id != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You do not have permission to match "
                "candidates for this job"
            ),
        )

    # -----------------------------------------------------
    # 4. Run recruiter matching workflow
    # -----------------------------------------------------

    return recruiter_matching_service.rank_candidates(
        db=db,
        job=job,
    )


# ---------------------------------------------------------
# Recruiter → Candidate Matching + AI Explanation
# ---------------------------------------------------------

@router.post(
    "/{job_id}/candidates/match/explain",
)
def explain_candidates_for_job(
    job_id: UUID,
    explanation_limit: int = Query(
        default=5,
        ge=1,
        description=(
            "Number of top-ranked candidates that should "
            "receive an AI-generated match explanation."
        ),
    ),
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # 1. Get recruiter profile
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # 2. Get active job
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # 3. Verify job ownership
    # -----------------------------------------------------

    if job.recruiter_id != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You do not have permission to explain "
                "candidates for this job"
            ),
        )

    # -----------------------------------------------------
    # 4. Run matching + explanation workflow
    # -----------------------------------------------------

    return recruiter_matching_service.rank_and_explain_candidates(
        db=db,
        job=job,
        explanation_limit=explanation_limit,
    )