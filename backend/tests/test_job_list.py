from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)


def test_job_list_returns_only_active_jobs():
    db = SessionLocal()

    recruiter_user = None
    recruiter_profile = None
    active_job = None
    inactive_job = None

    email = f"job-list-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary recruiter user
        # ---------------------------------------------------------
        recruiter_user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        db.add(recruiter_user)
        db.commit()
        db.refresh(recruiter_user)

        # ---------------------------------------------------------
        # Create recruiter profile
        # ---------------------------------------------------------
        recruiter_profile = Recruiter(
            user_id=recruiter_user.id,
            first_name="Test",
            last_name="Recruiter",
            job_title="Talent Acquisition Specialist",
            location="India",
        )

        db.add(recruiter_profile)
        db.commit()
        db.refresh(recruiter_profile)

        # ---------------------------------------------------------
        # Create active job
        # ---------------------------------------------------------
        active_job = Job(
            recruiter_id=recruiter_profile.id,
            title="Active Python Developer",
            description="Active job for integration testing.",
            location="Remote",
            employment_type="full_time",
            experience_level="mid",
            salary_min=800000,
            salary_max=1400000,
            is_active=True,
        )

        # ---------------------------------------------------------
        # Create inactive job
        # ---------------------------------------------------------
        inactive_job = Job(
            recruiter_id=recruiter_profile.id,
            title="Inactive Python Developer",
            description="Inactive job for integration testing.",
            location="Remote",
            employment_type="full_time",
            experience_level="senior",
            salary_min=1000000,
            salary_max=1600000,
            is_active=False,
        )

        db.add_all([active_job, inactive_job])
        db.commit()

        db.refresh(active_job)
        db.refresh(inactive_job)

        # ---------------------------------------------------------
        # GET /jobs
        # ---------------------------------------------------------
        response = client.get("/jobs")

        assert response.status_code == 200

        data = response.json()

        # ---------------------------------------------------------
        # Verify active job is returned
        # ---------------------------------------------------------
        active_job_ids = {
            job["id"]
            for job in data
        }

        assert str(active_job.id) in active_job_ids

        # ---------------------------------------------------------
        # Verify inactive job is NOT returned
        # ---------------------------------------------------------
        assert str(inactive_job.id) not in active_job_ids

        # ---------------------------------------------------------
        # Verify every returned job is active
        # ---------------------------------------------------------
        assert all(
            job["is_active"] is True
            for job in data
        )

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if active_job:
            db.delete(active_job)

        if inactive_job:
            db.delete(inactive_job)

        if recruiter_profile:
            db.delete(recruiter_profile)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()