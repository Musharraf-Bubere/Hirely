from uuid import uuid4

import pytest

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User, UserRole
from app.services.resume import activate_resume, create_resume


def create_test_candidate(db, email_prefix: str):
    user = User(
        email=f"{email_prefix}-{uuid4()}@example.com",
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
        bio="Resume activation test candidate.",
        location="India",
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return user, candidate


def test_activate_resume_deactivates_previous_active_resume():
    db = SessionLocal()

    user = None
    candidate = None
    resume_one = None
    resume_two = None

    try:
        user, candidate = create_test_candidate(
            db,
            "resume-activation",
        )

        resume_one = create_resume(
            db=db,
            candidate=candidate,
            original_filename="resume_v1.pdf",
            file_path="test_data/resume_v1.pdf",
        )

        resume_two = create_resume(
            db=db,
            candidate=candidate,
            original_filename="resume_v2.pdf",
            file_path="test_data/resume_v2.pdf",
        )

        resume_one.is_active = True
        db.commit()
        db.refresh(resume_one)

        result = activate_resume(
            db=db,
            candidate=candidate,
            resume=resume_two,
        )

        assert result.id == resume_two.id
        assert result.is_active is True

        db.refresh(resume_one)

        assert resume_one.is_active is False

    finally:
        if resume_one:
            db.delete(resume_one)

        if resume_two:
            db.delete(resume_two)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_activate_resume_rejects_resume_belonging_to_another_candidate():
    db = SessionLocal()

    user_one = None
    candidate_one = None
    user_two = None
    candidate_two = None
    resume = None

    try:
        user_one, candidate_one = create_test_candidate(
            db,
            "resume-owner",
        )

        user_two, candidate_two = create_test_candidate(
            db,
            "resume-other",
        )

        resume = create_resume(
            db=db,
            candidate=candidate_one,
            original_filename="candidate_one.pdf",
            file_path="test_data/candidate_one.pdf",
        )

        with pytest.raises(
            ValueError,
            match="Resume does not belong to candidate",
        ):
            activate_resume(
                db=db,
                candidate=candidate_two,
                resume=resume,
            )

        db.refresh(resume)

        assert resume.is_active is False

    finally:
        if resume:
            db.delete(resume)

        if candidate_one:
            db.delete(candidate_one)

        if candidate_two:
            db.delete(candidate_two)

        if user_one:
            db.delete(user_one)

        if user_two:
            db.delete(user_two)

        db.commit()
        db.close()