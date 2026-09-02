from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_candidate
from app.db.session import get_db
from app.models.candidate import Candidate
from app.models.user import User
from app.models.skill import Skill
from app.models.candidate_skill import CandidateSkill
from app.schemas.skill import SkillCreateRequest, SkillResponse
from app.services.skill import get_or_create_skill
from app.services.candidate_skill import add_candidate_skill


router = APIRouter(
    prefix="/candidate/skills",
    tags=["Candidate Skills"],
)


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_skill_to_candidate(
    data: SkillCreateRequest,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    # ---------------------------------------------------------
    # Find candidate profile
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Find existing skill or create a new one
    # ---------------------------------------------------------
    skill = get_or_create_skill(
        db=db,
        data=data,
    )

    # ---------------------------------------------------------
    # Create Candidate ↔ Skill association
    # ---------------------------------------------------------
    try:
        add_candidate_skill(
            db=db,
            candidate=candidate,
            skill=skill,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return skill


@router.get(
    "",
    response_model=list[SkillResponse],
)
def get_candidate_skills(
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    # ---------------------------------------------------------
    # Find candidate profile
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Get candidate skills
    # ---------------------------------------------------------
    candidate_skills = (
        db.query(CandidateSkill)
        .filter(CandidateSkill.candidate_id == candidate.id)
        .all()
    )

    return [candidate_skill.skill for candidate_skill in candidate_skills]


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_skill_from_candidate(
    skill_id: UUID,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    # ---------------------------------------------------------
    # Find candidate profile
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # Find candidate-skill association
    # ---------------------------------------------------------
    candidate_skill = (
        db.query(CandidateSkill)
        .filter(
            CandidateSkill.candidate_id == candidate.id,
            CandidateSkill.skill_id == skill_id,
        )
        .first()
    )

    if not candidate_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found for candidate",
        )

    # ---------------------------------------------------------
    # Remove association
    # ---------------------------------------------------------
    db.delete(candidate_skill)
    db.commit()

    return None