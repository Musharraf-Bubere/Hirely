from uuid import uuid4

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.candidate_skill import CandidateSkill
from app.models.resume import Resume
from app.models.skill import Skill
from app.models.user import User, UserRole
from app.services.resume_skill import sync_resume_skills_to_candidate


def create_test_candidate(db):
    user = User(
        email=f"resume-skill-{uuid4()}@example.com",
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
        headline="AI Engineer",
        bio="Resume skill synchronization test.",
        location="India",
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return user, candidate


def test_sync_resume_skills_to_candidate():
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    try:
        # ---------------------------------------------------------
        # Create test candidate
        # ---------------------------------------------------------
        user, candidate = create_test_candidate(db)

        # ---------------------------------------------------------
        # Create parsed resume
        # ---------------------------------------------------------
        resume = Resume(
            candidate_id=candidate.id,
            original_filename="test_resume.pdf",
            file_path="test_data/test_resume.pdf",
            parsing_status="COMPLETED",
            parsed_data={
                "name": "Test Candidate",
                "email": "test@example.com",
                "skills": [
                    "Python",
                    "SQL",
                    "FastAPI",
                ],
            },
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # ---------------------------------------------------------
        # Synchronize resume skills
        # ---------------------------------------------------------
        result = sync_resume_skills_to_candidate(
            db=db,
            candidate=candidate,
            resume=resume,
        )

        # ---------------------------------------------------------
        # Verify result
        # ---------------------------------------------------------
        assert len(result) == 3

        # ---------------------------------------------------------
        # Verify CandidateSkill associations
        # ---------------------------------------------------------
        candidate_skills = (
            db.query(CandidateSkill)
            .filter(
                CandidateSkill.candidate_id == candidate.id,
            )
            .all()
        )

        assert len(candidate_skills) == 3

        # ---------------------------------------------------------
        # Verify skill names
        # ---------------------------------------------------------
        skill_names = {
            candidate_skill.skill.name
            for candidate_skill in candidate_skills
        }

        assert skill_names == {
            "Python",
            "SQL",
            "FastAPI",
        }

    finally:
        # ---------------------------------------------------------
        # Cleanup resume
        # ---------------------------------------------------------
        if resume:
            db.delete(resume)

        # ---------------------------------------------------------
        # Cleanup CandidateSkill associations
        # ---------------------------------------------------------
        if candidate:
            db.query(CandidateSkill).filter(
                CandidateSkill.candidate_id == candidate.id
            ).delete(
                synchronize_session=False,
            )

        db.flush()

        # ---------------------------------------------------------
        # Cleanup candidate and user
        # ---------------------------------------------------------
        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_sync_resume_skills_reuses_existing_skills_and_associations():
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    try:
        # ---------------------------------------------------------
        # Create test candidate
        # ---------------------------------------------------------
        user, candidate = create_test_candidate(db)

        # ---------------------------------------------------------
        # Find existing Python skill
        # ---------------------------------------------------------
        existing_skill = (
            db.query(Skill)
            .filter(
                Skill.name.ilike("Python"),
            )
            .first()
        )

        # ---------------------------------------------------------
        # Create Python skill only if it does not exist
        # ---------------------------------------------------------
        if not existing_skill:
            existing_skill = Skill(
                name="Python",
            )

            db.add(existing_skill)
            db.commit()
            db.refresh(existing_skill)

        # ---------------------------------------------------------
        # Create existing CandidateSkill association
        # ---------------------------------------------------------
        existing_candidate_skill = CandidateSkill(
            candidate_id=candidate.id,
            skill_id=existing_skill.id,
        )

        db.add(existing_candidate_skill)
        db.commit()

        # ---------------------------------------------------------
        # Create parsed resume
        # ---------------------------------------------------------
        resume = Resume(
            candidate_id=candidate.id,
            original_filename="test_resume.pdf",
            file_path="test_data/test_resume.pdf",
            parsing_status="COMPLETED",
            parsed_data={
                "skills": [
                    "Python",
                    " SQL ",
                    "python",
                ],
            },
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # ---------------------------------------------------------
        # Synchronize resume skills
        # ---------------------------------------------------------
        result = sync_resume_skills_to_candidate(
            db=db,
            candidate=candidate,
            resume=resume,
        )

        # ---------------------------------------------------------
        # Three parsed skill entries were processed
        # ---------------------------------------------------------
        assert len(result) == 3

        # ---------------------------------------------------------
        # Verify only two CandidateSkill associations exist
        #
        # Python → existing association reused
        # SQL → new association created
        # python → same Python association reused
        # ---------------------------------------------------------
        candidate_skills = (
            db.query(CandidateSkill)
            .filter(
                CandidateSkill.candidate_id == candidate.id,
            )
            .all()
        )

        assert len(candidate_skills) == 2

        # ---------------------------------------------------------
        # Verify skill names
        # ---------------------------------------------------------
        skill_names = {
            candidate_skill.skill.name
            for candidate_skill in candidate_skills
        }

        assert skill_names == {
            "Python",
            "SQL",
        }

        # ---------------------------------------------------------
        # Verify only one Python Skill exists
        # ---------------------------------------------------------
        python_skills = (
            db.query(Skill)
            .filter(
                Skill.name.ilike("python"),
            )
            .all()
        )

        assert len(python_skills) == 1

    finally:
        # ---------------------------------------------------------
        # Cleanup resume
        # ---------------------------------------------------------
        if resume:
            db.delete(resume)

        # ---------------------------------------------------------
        # Cleanup CandidateSkill associations
        # ---------------------------------------------------------
        if candidate:
            db.query(CandidateSkill).filter(
                CandidateSkill.candidate_id == candidate.id
            ).delete(
                synchronize_session=False,
            )

        db.flush()

        # ---------------------------------------------------------
        # Cleanup candidate and user
        # ---------------------------------------------------------
        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_sync_resume_skills_requires_parsed_resume():
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    try:
        # ---------------------------------------------------------
        # Create test candidate
        # ---------------------------------------------------------
        user, candidate = create_test_candidate(db)

        # ---------------------------------------------------------
        # Create unparsed resume
        # ---------------------------------------------------------
        resume = Resume(
            candidate_id=candidate.id,
            original_filename="test_resume.pdf",
            file_path="test_data/test_resume.pdf",
            parsing_status="PENDING",
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # ---------------------------------------------------------
        # Attempt synchronization
        # ---------------------------------------------------------
        try:
            sync_resume_skills_to_candidate(
                db=db,
                candidate=candidate,
                resume=resume,
            )

            assert False, "Expected ValueError was not raised"

        except ValueError as exc:
            assert str(exc) == "Resume has not been parsed"

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_sync_resume_skills_rejects_other_candidates_resume():
    db = SessionLocal()

    user_one = None
    candidate_one = None

    user_two = None
    candidate_two = None

    resume = None

    try:
        # ---------------------------------------------------------
        # Create two candidates
        # ---------------------------------------------------------
        user_one, candidate_one = create_test_candidate(db)
        user_two, candidate_two = create_test_candidate(db)

        # ---------------------------------------------------------
        # Create resume belonging to Candidate 1
        # ---------------------------------------------------------
        resume = Resume(
            candidate_id=candidate_one.id,
            original_filename="private_resume.pdf",
            file_path="test_data/private_resume.pdf",
            parsing_status="COMPLETED",
            parsed_data={
                "skills": [
                    "Python",
                ],
            },
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # ---------------------------------------------------------
        # Candidate 2 attempts to synchronize Candidate 1's resume
        # ---------------------------------------------------------
        try:
            sync_resume_skills_to_candidate(
                db=db,
                candidate=candidate_two,
                resume=resume,
            )

            assert False, "Expected ValueError was not raised"

        except ValueError as exc:
            assert str(exc) == "Resume does not belong to candidate"

    finally:
        # ---------------------------------------------------------
        # Cleanup resume
        # ---------------------------------------------------------
        if resume:
            db.delete(resume)

        # ---------------------------------------------------------
        # Cleanup Candidate 2
        # ---------------------------------------------------------
        if candidate_two:
            db.query(CandidateSkill).filter(
                CandidateSkill.candidate_id == candidate_two.id
            ).delete(
                synchronize_session=False,
            )

            db.delete(candidate_two)

        if user_two:
            db.delete(user_two)

        # ---------------------------------------------------------
        # Cleanup Candidate 1
        # ---------------------------------------------------------
        if candidate_one:
            db.query(CandidateSkill).filter(
                CandidateSkill.candidate_id == candidate_one.id
            ).delete(
                synchronize_session=False,
            )

            db.delete(candidate_one)

        if user_one:
            db.delete(user_one)

        db.commit()
        db.close()