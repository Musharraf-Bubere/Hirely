from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.db.session import SessionLocal
from app.main import app
from app.models import Candidate, User
from app.schemas.auth import RegisterRequest
from app.services.auth import register_user


client = TestClient(app)


def test_candidate_can_update_profile():
    db = SessionLocal()

    test_email = f"candidate-profile-update-{uuid4()}@example.com"

    user = None
    candidate = None

    try:
        # ---------------------------------------------------------
        # Create candidate user and profile
        # ---------------------------------------------------------
        data = RegisterRequest(
            first_name="Old",
            last_name="Name",
            email=test_email,
            password="secret123",
            role="candidate",
        )

        user = register_user(db, data)

        # ---------------------------------------------------------
        # Get candidate profile created during registration
        # ---------------------------------------------------------
        candidate = (
            db.query(Candidate)
            .filter(Candidate.user_id == user.id)
            .first()
        )

        assert candidate is not None

        # ---------------------------------------------------------
        # Set initial profile data
        # ---------------------------------------------------------
        candidate.headline = "Old Headline"
        candidate.bio = "Old bio"
        candidate.location = "Old Location"

        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            str(user.id),
            user.role.value,
        )

        headers = {
            "Authorization": f"Bearer {token}",
        }

        # ---------------------------------------------------------
        # Update candidate profile
        # ---------------------------------------------------------
        response = client.patch(
            "/candidate/profile",
            headers=headers,
            json={
                "first_name": "Musharraf",
                "last_name": "Bubere",
                "headline": "Data Scientist | Machine Learning Engineer",
                "bio": (
                    "Data Science professional with experience "
                    "in Python, Machine Learning, Generative AI, "
                    "SQL, and analytics."
                ),
                "location": "Mumbai, India",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # API response assertions
        # ---------------------------------------------------------
        assert response.status_code == 200

        result = response.json()

        assert result["id"] == str(candidate.id)
        assert result["email"] == test_email

        assert result["first_name"] == "Musharraf"
        assert result["last_name"] == "Bubere"

        assert (
            result["headline"]
            == "Data Scientist | Machine Learning Engineer"
        )

        assert (
            result["bio"]
            == (
                "Data Science professional with experience "
                "in Python, Machine Learning, Generative AI, "
                "SQL, and analytics."
            )
        )

        assert result["location"] == "Mumbai, India"

        # ---------------------------------------------------------
        # Verify database persistence
        # ---------------------------------------------------------
        db.refresh(candidate)

        assert candidate.first_name == "Musharraf"
        assert candidate.last_name == "Bubere"

        assert (
            candidate.headline
            == "Data Scientist | Machine Learning Engineer"
        )

        assert (
            candidate.bio
            == (
                "Data Science professional with experience "
                "in Python, Machine Learning, Generative AI, "
                "SQL, and analytics."
            )
        )

        assert candidate.location == "Mumbai, India"

        print("Candidate profile update test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup candidate profile
        # ---------------------------------------------------------
        if candidate:
            db.delete(candidate)

        # ---------------------------------------------------------
        # Cleanup user
        # ---------------------------------------------------------
        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary candidate profile update data cleaned up.")