from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.user import User, UserRole


client = TestClient(app)


def test_candidate_can_get_own_profile():
    db = SessionLocal()

    user = None
    candidate = None

    email = f"candidate-profile-{uuid4()}@example.com"

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
            bio="Candidate profile integration test.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Get candidate profile
        # Expected: 200
        # ---------------------------------------------------------
        response = client.get(
            "/candidate/profile",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == str(user.id)
        assert data["email"] == email
        assert data["role"] == "candidate"
        assert data["is_active"] is True
        assert data["first_name"] == "Test"
        assert data["last_name"] == "Candidate"
        assert data["headline"] == "Python Developer"
        assert data["bio"] == "Candidate profile integration test."
        assert data["location"] == "India"

        print("Candidate profile test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary candidate profile data cleaned up.")