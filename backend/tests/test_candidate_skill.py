from uuid import uuid4

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.candidate_skill import CandidateSkill
from app.models.skill import Skill
from app.models.user import User, UserRole
from app.services.candidate_skill import add_candidate_skill


def test_add_candidate_skill():
    db = SessionLocal()

    user = None
    candidate = None
    skill = None
    candidate_skill = None

    email = f"candidate-skill-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary candidate user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create candidate profile
        # ---------------------------------------------------------
        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create temporary skill
        # ---------------------------------------------------------
        skill = Skill(
            name=f"Python-{uuid4()}",
        )

        db.add(skill)
        db.commit()
        db.refresh(skill)

        # ---------------------------------------------------------
        # Add skill to candidate
        # ---------------------------------------------------------
        candidate_skill = add_candidate_skill(
            db=db,
            candidate=candidate,
            skill=skill,
        )

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert candidate_skill is not None
        assert candidate_skill.candidate_id == candidate.id
        assert candidate_skill.skill_id == skill.id

        # Verify association exists in database
        saved_association = (
            db.query(CandidateSkill)
            .filter(
                CandidateSkill.candidate_id == candidate.id,
                CandidateSkill.skill_id == skill.id,
            )
            .first()
        )

        assert saved_association is not None

        print("Candidate skill service test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if candidate_skill:
            db.delete(candidate_skill)

        if skill:
            db.delete(skill)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary candidate skill data cleaned up.")


def test_add_duplicate_candidate_skill():
    db = SessionLocal()

    user = None
    candidate = None
    skill = None
    candidate_skill = None

    email = f"candidate-duplicate-skill-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary candidate user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create candidate profile
        # ---------------------------------------------------------
        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create temporary skill
        # ---------------------------------------------------------
        skill = Skill(
            name=f"Python-{uuid4()}",
        )

        db.add(skill)
        db.commit()
        db.refresh(skill)

        # ---------------------------------------------------------
        # Add skill for the first time
        # ---------------------------------------------------------
        candidate_skill = add_candidate_skill(
            db=db,
            candidate=candidate,
            skill=skill,
        )

        assert candidate_skill is not None

        # ---------------------------------------------------------
        # Try adding the same skill again
        # Expected: ValueError
        # ---------------------------------------------------------
        try:
            add_candidate_skill(
                db=db,
                candidate=candidate,
                skill=skill,
            )

            assert False, "Expected ValueError was not raised"

        except ValueError as exc:
            assert str(exc) == "Skill already added to candidate"

        print("Duplicate candidate skill test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if candidate_skill:
            db.delete(candidate_skill)

        if skill:
            db.delete(skill)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary duplicate candidate skill data cleaned up.")