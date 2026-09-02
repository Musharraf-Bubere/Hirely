from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)


def test_job_detail_for_active_inactive_and_nonexistent_jobs():
    db = SessionLocal()

    recruiter_user = None
    recruiter_profile = None
    active_job = None
    inactive_job = None

    email = f"job-detail-{uuid4()}@example.com"

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
            description="Active job detail test.",
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
            description="Inactive job detail test.",
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
        # Existing active job
        # Expected: 200
        # ---------------------------------------------------------
        response = client.get(f"/jobs/{active_job.id}")

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == str(active_job.id)
        assert data["recruiter_id"] == str(recruiter_profile.id)
        assert data["title"] == "Active Python Developer"
        assert data["is_active"] is True

        # ---------------------------------------------------------
        # Existing inactive job
        # Expected: 404
        # ---------------------------------------------------------
        response = client.get(f"/jobs/{inactive_job.id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"

        # ---------------------------------------------------------
        # Nonexistent job
        # Expected: 404
        # ---------------------------------------------------------
        nonexistent_job_id = uuid4()

        response = client.get(f"/jobs/{nonexistent_job_id}")

        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"

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