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

candidate_email = f"duplicate-candidate-{uuid4()}@example.com"
recruiter_email = f"duplicate-recruiter-{uuid4()}@example.com"

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
    # Candidate profile
    # ---------------------------------------------------------
    candidate_profile = Candidate(
        user_id=candidate.id,
        first_name="Duplicate",
        last_name="Candidate",
        headline="Python Developer",
        bio="Duplicate application test candidate.",
        location="India",
    )

    # ---------------------------------------------------------
    # Recruiter profile
    # ---------------------------------------------------------
    recruiter_profile = Recruiter(
        user_id=recruiter.id,
        first_name="Duplicate",
        last_name="Recruiter",
        job_title="Recruiter",
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
        title="Python Developer",
        description="Duplicate application test job.",
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
    # First application
    # Expected: 201
    # ---------------------------------------------------------
    response = client.post(
        f"/jobs/{job.id}/apply",
        headers=headers,
    )

    print(
        "First application:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 201

    application = (
        db.query(Application)
        .filter(
            Application.candidate_id == candidate_profile.id,
            Application.job_id == job.id,
        )
        .first()
    )

    assert application is not None

    # ---------------------------------------------------------
    # Second application
    # Expected: 409
    # ---------------------------------------------------------
    response = client.post(
        f"/jobs/{job.id}/apply",
        headers=headers,
    )

    print(
        "Duplicate application:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "You have already applied to this job"
    )

    # ---------------------------------------------------------
    # Verify only one application exists
    # ---------------------------------------------------------
    application_count = (
        db.query(Application)
        .filter(
            Application.candidate_id == candidate_profile.id,
            Application.job_id == job.id,
        )
        .count()
    )

    assert application_count == 1

    print("Duplicate application protection passed.")
    print("Application count:", application_count)

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

    print("Temporary duplicate application test data cleaned up.")