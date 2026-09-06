from uuid import uuid4

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User, UserRole
from app.services.resume import (
    activate_resume,
    create_resume,
    get_active_resume,
)


def create_test_candidate(db):
    user = User(
        email=f"resume-retrieval-{uuid4()}@example.com",
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.CANDIDATE,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    candidate = Candidate(
        user_id=user.id,
        first_name="Test",
        last_name="Candidate",
        headline="Python Developer",
        bio="Resume retrieval test candidate.",
        location="India",
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return user, candidate


def test_get_active_resume_returns_active_resume():
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    try:
        user, candidate = create_test_candidate(db)

        resume = create_resume(
            db=db,
            candidate=candidate,
            original_filename="active_resume.pdf",
            file_path="test_data/active_resume.pdf",
        )

        activate_resume(
            db=db,
            candidate=candidate,
            resume=resume,
        )

        result = get_active_resume(
            db=db,
            candidate=candidate,
        )

        assert result is not None
        assert result.id == resume.id
        assert result.candidate_id == candidate.id
        assert result.is_active is True

    finally:
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_get_active_resume_returns_none_when_no_active_resume_exists():
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    try:
        user, candidate = create_test_candidate(db)

        resume = create_resume(
            db=db,
            candidate=candidate,
            original_filename="inactive_resume.pdf",
            file_path="test_data/inactive_resume.pdf",
        )

        result = get_active_resume(
            db=db,
            candidate=candidate,
        )

        assert result is None

    finally:
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()