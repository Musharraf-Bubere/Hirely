from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)
db = SessionLocal()

candidate = None
candidate_profile = None
recruiter = None
recruiter_profile = None
job = None
application = None

candidate_email = f"application-candidate-{uuid4()}@example.com"
recruiter_email = f"application-recruiter-{uuid4()}@example.com"

try:
    # ---------------------------------------------------------
    # Create temporary candidate user
    # ---------------------------------------------------------
    candidate = User(
        email=candidate_email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.CANDIDATE,
    )

    # ---------------------------------------------------------
    # Create temporary recruiter user
    # ---------------------------------------------------------
    recruiter = User(
        email=recruiter_email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.RECRUITER,
    )

    db.add_all([candidate, recruiter])
    db.commit()

    db.refresh(candidate)
    db.refresh(recruiter)

    # ---------------------------------------------------------
    # Create candidate profile
    # ---------------------------------------------------------
    candidate_profile = Candidate(
        user_id=candidate.id,
        first_name="Test",
        last_name="Candidate",
        headline="Python Developer",
        bio="Application integration test candidate.",
        location="India",
    )

    # ---------------------------------------------------------
    # Create recruiter profile
    # ---------------------------------------------------------
    recruiter_profile = Recruiter(
        user_id=recruiter.id,
        first_name="Test",
        last_name="Recruiter",
        job_title="Talent Acquisition Specialist",
        location="India",
    )

    db.add_all([candidate_profile, recruiter_profile])
    db.commit()

    db.refresh(candidate_profile)
    db.refresh(recruiter_profile)

    # ---------------------------------------------------------
    # Create active job
    # ---------------------------------------------------------
    job = Job(
        recruiter_id=recruiter_profile.id,
        title="Python Backend Developer",
        description="Build backend services for Hirely.",
        location="Remote",
        employment_type="full_time",
        experience_level="mid",
        salary_min=800000,
        salary_max=1400000,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # ---------------------------------------------------------
    # Generate JWTs
    # ---------------------------------------------------------
    candidate_token = create_access_token(
        user_id=str(candidate.id),
        role=candidate.role.value,
    )

    recruiter_token = create_access_token(
        user_id=str(recruiter.id),
        role=recruiter.role.value,
    )

    def auth_header(token: str) -> dict:
        return {
            "Authorization": f"Bearer {token}",
        }

    # ---------------------------------------------------------
    # Candidate → Apply to job
    # Expected: 201
    # ---------------------------------------------------------
    response = client.post(
        f"/jobs/{job.id}/apply",
        headers=auth_header(candidate_token),
    )

    print(
        "Candidate → Apply to job:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 201

    data = response.json()

    assert data["candidate_id"] == str(candidate_profile.id)
    assert data["job_id"] == str(job.id)
    assert data["status"] == "applied"

    # ---------------------------------------------------------
    # Verify application persisted
    # ---------------------------------------------------------
    application = (
        db.query(Application)
        .filter(
            Application.candidate_id == candidate_profile.id,
            Application.job_id == job.id,
        )
        .first()
    )

    assert application is not None
    assert application.status.value == "applied"

    print("Application persisted successfully.")

    # ---------------------------------------------------------
    # Recruiter → Apply to job
    # Expected: 403
    # ---------------------------------------------------------
    response = client.post(
        f"/jobs/{job.id}/apply",
        headers=auth_header(recruiter_token),
    )

    print(
        "Recruiter → Apply to job:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 403

    print("Application creation tests passed.")

finally:
    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------
    if application:
        db.delete(application)

    if job:
        db.delete(job)

    if candidate_profile:
        db.delete(candidate_profile)

    if recruiter_profile:
        db.delete(recruiter_profile)

    if candidate:
        db.delete(candidate)

    if recruiter:
        db.delete(recruiter)

    db.commit()
    db.close()

    print("Temporary application test data cleaned up.")