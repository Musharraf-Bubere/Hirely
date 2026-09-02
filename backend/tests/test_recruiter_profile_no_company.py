from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)


def test_recruiter_profile_without_company():
    db = SessionLocal()

    user = None
    recruiter = None

    email = f"recruiter-no-company-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create recruiter user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create recruiter WITHOUT a company
        # ---------------------------------------------------------
        recruiter = Recruiter(
            user_id=user.id,
            company_id=None,
            first_name="Independent",
            last_name="Recruiter",
            job_title="Talent Acquisition Specialist",
            location="India",
        )

        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # GET /recruiter/profile
        # Expected: 200
        # ---------------------------------------------------------
        response = client.get(
            "/recruiter/profile",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert response.status_code == 200

        data = response.json()

        # ---------------------------------------------------------
        # Verify user data
        # ---------------------------------------------------------
        assert data["id"] == str(user.id)
        assert data["email"] == email
        assert data["role"] == "recruiter"
        assert data["is_active"] is True

        # ---------------------------------------------------------
        # Verify recruiter data
        # ---------------------------------------------------------
        assert data["first_name"] == "Independent"
        assert data["last_name"] == "Recruiter"
        assert data["job_title"] == "Talent Acquisition Specialist"
        assert data["location"] == "India"

        # ---------------------------------------------------------
        # Verify company is optional
        # ---------------------------------------------------------
        assert data["company"] is None

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if recruiter:
            db.delete(recruiter)

        if user:
            db.delete(user)

        db.commit()
        db.close()