from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
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

candidate_email = f"inactive-job-candidate-{uuid4()}@example.com"
recruiter_email = f"inactive-job-recruiter-{uuid4()}@example.com"

try:
    # ---------------------------------------------------------
    # Create candidate
    # ---------------------------------------------------------
    candidate = User(
        email=candidate_email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.CANDIDATE,
    )

    # ---------------------------------------------------------
    # Create recruiter
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
        first_name="Inactive",
        last_name="Candidate",
        headline="Python Developer",
        bio="Inactive job application test candidate.",
        location="India",
    )

    # ---------------------------------------------------------
    # Create recruiter profile
    # ---------------------------------------------------------
    recruiter_profile = Recruiter(
        user_id=recruiter.id,
        first_name="Inactive",
        last_name="Recruiter",
        job_title="Recruiter",
        location="India",
    )

    db.add_all([candidate_profile, recruiter_profile])
    db.commit()

    db.refresh(candidate_profile)
    db.refresh(recruiter_profile)

    # ---------------------------------------------------------
    # Create inactive job
    # ---------------------------------------------------------
    job = Job(
        recruiter_id=recruiter_profile.id,
        title="Closed Python Developer Position",
        description="This job is no longer accepting applications.",
        location="Remote",
        employment_type="full_time",
        experience_level="mid",
        salary_min=800000,
        salary_max=1400000,
        is_active=False,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # ---------------------------------------------------------
    # Generate candidate JWT
    # ---------------------------------------------------------
    candidate_token = create_access_token(
        user_id=str(candidate.id),
        role=candidate.role.value,
    )

    headers = {
        "Authorization": f"Bearer {candidate_token}",
    }

    # ---------------------------------------------------------
    # Candidate → Apply to inactive job
    # Expected: 404
    # ---------------------------------------------------------
    response = client.post(
        f"/jobs/{job.id}/apply",
        headers=headers,
    )

    print(
        "Candidate → Apply to inactive job:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"

    print("Inactive job application protection passed.")

finally:
    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------
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

    print("Temporary inactive job test data cleaned up.")