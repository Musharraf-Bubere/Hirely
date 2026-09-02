from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)


def test_recruiter_can_create_job_and_candidate_cannot():
    db = SessionLocal()

    recruiter_user = None
    recruiter_profile = None
    candidate_user = None
    job = None

    recruiter_email = f"job-recruiter-{uuid4()}@example.com"
    candidate_email = f"job-candidate-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary recruiter user
        # ---------------------------------------------------------
        recruiter_user = User(
            email=recruiter_email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        # ---------------------------------------------------------
        # Create temporary candidate user
        # ---------------------------------------------------------
        candidate_user = User(
            email=candidate_email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add_all([recruiter_user, candidate_user])
        db.commit()

        db.refresh(recruiter_user)
        db.refresh(candidate_user)

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
        # Generate JWTs
        # ---------------------------------------------------------
        recruiter_token = create_access_token(
            user_id=str(recruiter_user.id),
            role=recruiter_user.role.value,
        )

        candidate_token = create_access_token(
            user_id=str(candidate_user.id),
            role=candidate_user.role.value,
        )

        job_data = {
            "title": "Python Backend Developer",
            "description": "Build scalable backend services for Hirely.",
            "location": "Remote",
            "employment_type": "full_time",
            "experience_level": "mid",
            "salary_min": 800000,
            "salary_max": 1400000,
        }

        # ---------------------------------------------------------
        # Recruiter → Create Job
        # Expected: 201
        # ---------------------------------------------------------
        response = client.post(
            "/jobs",
            json=job_data,
            headers={
                "Authorization": f"Bearer {recruiter_token}",
            },
        )

        print("Recruiter → Create job:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 201

        data = response.json()

        assert data["title"] == job_data["title"]
        assert data["description"] == job_data["description"]
        assert data["location"] == job_data["location"]
        assert data["employment_type"] == job_data["employment_type"]
        assert data["experience_level"] == job_data["experience_level"]
        assert data["salary_min"] == job_data["salary_min"]
        assert data["salary_max"] == job_data["salary_max"]
        assert data["is_active"] is True
        assert data["recruiter_id"] == str(recruiter_profile.id)

        # ---------------------------------------------------------
        # Verify job exists in database
        # ---------------------------------------------------------
        job = (
            db.query(Job)
            .filter(Job.id == data["id"])
            .first()
        )

        assert job is not None
        assert str(job.id) == data["id"]

        # ---------------------------------------------------------
        # Candidate → Create Job
        # Expected: 403
        # ---------------------------------------------------------
        response = client.post(
            "/jobs",
            json=job_data,
            headers={
                "Authorization": f"Bearer {candidate_token}",
            },
        )

        print("Candidate → Create job:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 403

        print("Job creation tests passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if job:
            db.delete(job)

        if recruiter_profile:
            db.delete(recruiter_profile)

        if recruiter_user:
            db.delete(recruiter_user)

        if candidate_user:
            db.delete(candidate_user)

        db.commit()
        db.close()

        print("Temporary job test data cleaned up.")