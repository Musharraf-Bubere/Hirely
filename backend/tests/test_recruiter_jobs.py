from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)


def test_recruiter_can_get_own_jobs():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    own_job = None
    other_user = None
    other_recruiter = None
    other_job = None

    recruiter_email = (
        f"recruiter-jobs-{uuid4()}@example.com"
    )

    other_email = (
        f"other-recruiter-jobs-{uuid4()}@example.com"
    )

    try:
        # ---------------------------------------------------------
        # Create recruiter user
        # ---------------------------------------------------------
        recruiter_user = User(
            email=recruiter_email,
            password_hash=hash_password(
                "TestPassword123!"
            ),
            role=UserRole.RECRUITER,
        )

        db.add(recruiter_user)
        db.commit()
        db.refresh(recruiter_user)

        # ---------------------------------------------------------
        # Create recruiter profile
        # ---------------------------------------------------------
        recruiter = Recruiter(
            user_id=recruiter_user.id,
            first_name="Test",
            last_name="Recruiter",
            job_title="Talent Acquisition Specialist",
            location="India",
        )

        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        # ---------------------------------------------------------
        # Create recruiter's own job
        # ---------------------------------------------------------
        own_job = Job(
            recruiter_id=recruiter.id,
            title="Python Backend Developer",
            description="Recruiter's own test job.",
            location="Mumbai",
            employment_type="full_time",
            experience_level="mid",
            salary_min=800000,
            salary_max=1400000,
            is_active=True,
        )

        db.add(own_job)
        db.commit()
        db.refresh(own_job)

        # ---------------------------------------------------------
        # Create another recruiter user
        # ---------------------------------------------------------
        other_user = User(
            email=other_email,
            password_hash=hash_password(
                "TestPassword123!"
            ),
            role=UserRole.RECRUITER,
        )

        db.add(other_user)
        db.commit()
        db.refresh(other_user)

        # ---------------------------------------------------------
        # Create another recruiter profile
        # ---------------------------------------------------------
        other_recruiter = Recruiter(
            user_id=other_user.id,
            first_name="Other",
            last_name="Recruiter",
            job_title="Hiring Manager",
            location="India",
        )

        db.add(other_recruiter)
        db.commit()
        db.refresh(other_recruiter)

        # ---------------------------------------------------------
        # Create another recruiter's job
        # ---------------------------------------------------------
        other_job = Job(
            recruiter_id=other_recruiter.id,
            title="Data Engineer",
            description="Another recruiter's test job.",
            location="Pune",
            employment_type="full_time",
            experience_level="mid",
            salary_min=900000,
            salary_max=1500000,
            is_active=True,
        )

        db.add(other_job)
        db.commit()
        db.refresh(other_job)

        # ---------------------------------------------------------
        # Generate access token for first recruiter
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(recruiter_user.id),
            role=recruiter_user.role.value,
        )

        # ---------------------------------------------------------
        # GET /recruiter/jobs
        # ---------------------------------------------------------
        response = client.get(
            "/recruiter/jobs",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # Verify successful response
        # ---------------------------------------------------------
        assert response.status_code == 200

        data = response.json()

        assert isinstance(data, list)

        # ---------------------------------------------------------
        # Verify only own job is returned
        # ---------------------------------------------------------
        returned_job_ids = {
            item["id"]
            for item in data
        }

        assert str(own_job.id) in returned_job_ids
        assert str(other_job.id) not in returned_job_ids

        # ---------------------------------------------------------
        # Verify returned job details
        # ---------------------------------------------------------
        returned_job = next(
            item
            for item in data
            if item["id"] == str(own_job.id)
        )

        assert (
            returned_job["recruiter_id"]
            == str(recruiter.id)
        )

        assert (
            returned_job["title"]
            == "Python Backend Developer"
        )

        assert (
            returned_job["description"]
            == "Recruiter's own test job."
        )

        assert returned_job["location"] == "Mumbai"
        assert returned_job["employment_type"] == "full_time"
        assert returned_job["experience_level"] == "mid"
        assert returned_job["salary_min"] == 800000
        assert returned_job["salary_max"] == 1400000
        assert returned_job["is_active"] is True

        print(
            "Recruiter own jobs endpoint test passed."
        )

    finally:
        # ---------------------------------------------------------
        # Cleanup jobs
        # ---------------------------------------------------------
        if own_job:
            db.delete(own_job)

        if other_job:
            db.delete(other_job)

        # ---------------------------------------------------------
        # Cleanup recruiter profiles
        # ---------------------------------------------------------
        if recruiter:
            db.delete(recruiter)

        if other_recruiter:
            db.delete(other_recruiter)

        # ---------------------------------------------------------
        # Cleanup users
        # ---------------------------------------------------------
        if recruiter_user:
            db.delete(recruiter_user)

        if other_user:
            db.delete(other_user)

        db.commit()
        db.close()

        print(
            "Temporary recruiter jobs test data cleaned up."
        )