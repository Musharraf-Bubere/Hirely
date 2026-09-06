from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User, UserRole


client = TestClient(app)


def test_candidate_can_activate_resume():
    db = SessionLocal()

    user = None
    candidate = None
    resume_one = None
    resume_two = None

    email = f"resume-activate-{uuid4()}@example.com"

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
            headline="AI Engineer",
            bio="Resume activation API integration test.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create two resume versions
        # Resume 1 starts active
        # Resume 2 starts inactive
        # ---------------------------------------------------------
        resume_one = Resume(
            candidate_id=candidate.id,
            original_filename="old_resume.pdf",
            file_path="test_data/old_resume.pdf",
            parsing_status="COMPLETED",
            is_active=True,
        )

        db.add(resume_one)
        db.commit()
        db.refresh(resume_one)

        resume_two = Resume(
            candidate_id=candidate.id,
            original_filename="new_resume.pdf",
            file_path="test_data/new_resume.pdf",
            parsing_status="COMPLETED",
            is_active=False,
        )

        db.add(resume_two)
        db.commit()
        db.refresh(resume_two)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Activate Resume 2
        # Expected: 200
        # ---------------------------------------------------------
        response = client.patch(
            f"/resumes/{resume_two.id}/activate",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 200

        data = response.json()

        # ---------------------------------------------------------
        # Verify API response
        # ---------------------------------------------------------
        assert data["id"] == str(resume_two.id)
        assert data["original_filename"] == "new_resume.pdf"
        assert data["parsing_status"] == "COMPLETED"
        assert data["is_active"] is True

        # Internal fields must not be exposed
        assert "candidate_id" not in data
        assert "file_path" not in data
        assert "parsed_data" not in data

        # ---------------------------------------------------------
        # Verify database state
        # ---------------------------------------------------------
        db.refresh(resume_one)
        db.refresh(resume_two)

        assert resume_one.is_active is False
        assert resume_two.is_active is True

        # ---------------------------------------------------------
        # Verify only one active resume exists
        # ---------------------------------------------------------
        active_resumes = (
            db.query(Resume)
            .filter(
                Resume.candidate_id == candidate.id,
                Resume.is_active.is_(True),
            )
            .all()
        )

        assert len(active_resumes) == 1
        assert active_resumes[0].id == resume_two.id

        print("Resume activation API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if resume_two:
            db.delete(resume_two)

        if resume_one:
            db.delete(resume_one)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary resume activation API data cleaned up.")