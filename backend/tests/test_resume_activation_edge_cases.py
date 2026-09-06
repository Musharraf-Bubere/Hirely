from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User, UserRole


client = TestClient(app)


def test_candidate_cannot_activate_nonexistent_resume():
    db = SessionLocal()

    user = None
    candidate = None

    email = f"resume-not-found-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create candidate user
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
            bio="Resume not found API test.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Generate token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Try to activate nonexistent resume
        # ---------------------------------------------------------
        fake_resume_id = uuid4()

        response = client.patch(
            f"/resumes/{fake_resume_id}/activate",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 404
        assert response.json()["detail"] == "Resume not found"

        print("Nonexistent resume test passed.")

    finally:
        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_candidate_cannot_activate_another_candidates_resume():
    db = SessionLocal()

    user_one = None
    candidate_one = None

    user_two = None
    candidate_two = None

    resume = None

    email_one = f"resume-owner-{uuid4()}@example.com"
    email_two = f"resume-attacker-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create first candidate
        # ---------------------------------------------------------
        user_one = User(
            email=email_one,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user_one)
        db.commit()
        db.refresh(user_one)

        candidate_one = Candidate(
            user_id=user_one.id,
            first_name="Resume",
            last_name="Owner",
            headline="AI Engineer",
            bio="Resume owner.",
            location="India",
        )

        db.add(candidate_one)
        db.commit()
        db.refresh(candidate_one)

        # ---------------------------------------------------------
        # Create second candidate
        # ---------------------------------------------------------
        user_two = User(
            email=email_two,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user_two)
        db.commit()
        db.refresh(user_two)

        candidate_two = Candidate(
            user_id=user_two.id,
            first_name="Resume",
            last_name="Attacker",
            headline="AI Engineer",
            bio="Another candidate.",
            location="India",
        )

        db.add(candidate_two)
        db.commit()
        db.refresh(candidate_two)

        # ---------------------------------------------------------
        # Create resume belonging to Candidate 1
        # ---------------------------------------------------------
        resume = Resume(
            candidate_id=candidate_one.id,
            original_filename="private_resume.pdf",
            file_path="test_data/private_resume.pdf",
            parsing_status="COMPLETED",
            is_active=False,
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # ---------------------------------------------------------
        # Generate token for Candidate 2
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user_two.id),
            role=user_two.role.value,
        )

        # ---------------------------------------------------------
        # Candidate 2 tries to activate Candidate 1's resume
        # ---------------------------------------------------------
        response = client.patch(
            f"/resumes/{resume.id}/activate",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 403
        assert response.json()["detail"] == "Resume does not belong to candidate"

        # ---------------------------------------------------------
        # Verify resume was not activated
        # ---------------------------------------------------------
        db.refresh(resume)

        assert resume.is_active is False

        print("Cross-candidate resume protection test passed.")

    finally:
        if resume:
            db.delete(resume)

        if candidate_two:
            db.delete(candidate_two)

        if user_two:
            db.delete(user_two)

        if candidate_one:
            db.delete(candidate_one)

        if user_one:
            db.delete(user_one)

        db.commit()
        db.close()


def test_unauthenticated_user_cannot_activate_resume():
    fake_resume_id = uuid4()

    response = client.patch(
        f"/resumes/{fake_resume_id}/activate",
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

    print("Unauthenticated resume activation test passed.")