from uuid import uuid4

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User, UserRole
from app.services.resume import create_resume


def test_create_resume():
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    email = f"resume-service-{uuid4()}@example.com"

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
            headline="Python Developer",
            bio="Resume service test candidate.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create resume
        # ---------------------------------------------------------
        resume = create_resume(
            db=db,
            candidate=candidate,
            original_filename="test_resume.pdf",
            file_path="test_data/test_resume.pdf",
        )

        # ---------------------------------------------------------
        # Verify returned resume
        # ---------------------------------------------------------
        assert resume.id is not None
        assert resume.candidate_id == candidate.id
        assert resume.original_filename == "test_resume.pdf"
        assert resume.file_path == "test_data/test_resume.pdf"
        assert resume.parsing_status == "PENDING"
        assert resume.is_active is False

        # ---------------------------------------------------------
        # Verify resume persisted in database
        # ---------------------------------------------------------
        persisted_resume = (
            db.query(Resume)
            .filter(
                Resume.id == resume.id,
            )
            .first()
        )

        assert persisted_resume is not None
        assert persisted_resume.candidate_id == candidate.id

        print("Resume persisted successfully.")

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

        print("Temporary resume test data cleaned up.")