from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.user import User
from app.schemas.candidate import (
    CandidateProfileCreate,
    CandidateProfileUpdate,
)


def create_candidate_profile(
    db: Session,
    user: User,
    data: CandidateProfileCreate,
) -> Candidate:
    existing_candidate = (
        db.query(Candidate)
        .filter(Candidate.user_id == user.id)
        .first()
    )

    if existing_candidate:
        raise ValueError("Candidate profile already exists")

    candidate = Candidate(
        user_id=user.id,
        first_name=data.first_name,
        last_name=data.last_name,
        headline=data.headline,
        bio=data.bio,
        location=data.location,
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


def update_candidate_profile(
    db: Session,
    user: User,
    data: CandidateProfileUpdate,
) -> Candidate:
    candidate = (
        db.query(Candidate)
        .filter(Candidate.user_id == user.id)
        .first()
    )

    if not candidate:
        raise ValueError("Candidate profile not found")

    candidate.first_name = data.first_name
    candidate.last_name = data.last_name
    candidate.headline = data.headline
    candidate.bio = data.bio
    candidate.location = data.location

    db.commit()
    db.refresh(candidate)

    return candidate


def get_candidates(db: Session) -> list[Candidate]:
    return db.query(Candidate).all()