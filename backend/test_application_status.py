from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.application import Application, ApplicationStatus
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)
db = SessionLocal()

candidate = None
candidate_profile = None

recruiter_a = None
recruiter_a_profile = None

recruiter_b = None
recruiter_b_profile = None

job_a = None
job_b = None

application_a = None
application_b = None

candidate_email = f"status-candidate-{uuid4()}@example.com"
recruiter_a_email = f"status-recruiter-a-{uuid4()}@example.com"
recruiter_b_email = f"status-recruiter-b-{uuid4()}@example.com"

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
    # Create recruiter A
    # ---------------------------------------------------------
    recruiter_a = User(
        email=recruiter_a_email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.RECRUITER,
    )

    # ---------------------------------------------------------
    # Create recruiter B
    # ---------------------------------------------------------
    recruiter_b = User(
        email=recruiter_b_email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.RECRUITER,
    )

    db.add_all([
        candidate,
        recruiter_a,
        recruiter_b,
    ])
    db.commit()

    db.refresh(candidate)
    db.refresh(recruiter_a)
    db.refresh(recruiter_b)

    # ---------------------------------------------------------
    # Candidate profile
    # ---------------------------------------------------------
    candidate_profile = Candidate(
        user_id=candidate.id,
        first_name="Status",
        last_name="Candidate",
        headline="Python Developer",
        bio="Application status test candidate.",
        location="India",
    )

    # ---------------------------------------------------------
    # Recruiter A profile
    # ---------------------------------------------------------
    recruiter_a_profile = Recruiter(
        user_id=recruiter_a.id,
        first_name="Recruiter",
        last_name="A",
        job_title="Senior Recruiter",
        location="India",
    )

    # ---------------------------------------------------------
    # Recruiter B profile
    # ---------------------------------------------------------
    recruiter_b_profile = Recruiter(
        user_id=recruiter_b.id,
        first_name="Recruiter",
        last_name="B",
        job_title="Senior Recruiter",
        location="India",
    )

    db.add_all([
        candidate_profile,
        recruiter_a_profile,
        recruiter_b_profile,
    ])
    db.commit()

    db.refresh(candidate_profile)
    db.refresh(recruiter_a_profile)
    db.refresh(recruiter_b_profile)

    # ---------------------------------------------------------
    # Recruiter A job
    # ---------------------------------------------------------
    job_a = Job(
        recruiter_id=recruiter_a_profile.id,
        title="Python Backend Developer",
        description="Recruiter A status test job.",
        location="Remote",
        employment_type="full_time",
        experience_level="mid",
        salary_min=800000,
        salary_max=1400000,
    )

    # ---------------------------------------------------------
    # Recruiter B job
    # ---------------------------------------------------------
    job_b = Job(
        recruiter_id=recruiter_b_profile.id,
        title="Data Engineer",
        description="Recruiter B status test job.",
        location="Remote",
        employment_type="full_time",
        experience_level="mid",
        salary_min=900000,
        salary_max=1500000,
    )

    db.add_all([
        job_a,
        job_b,
    ])
    db.commit()

    db.refresh(job_a)
    db.refresh(job_b)

    # ---------------------------------------------------------
    # Application for Recruiter A's job
    # ---------------------------------------------------------
    application_a = Application(
        candidate_id=candidate_profile.id,
        job_id=job_a.id,
        status=ApplicationStatus.APPLIED,
    )

    # ---------------------------------------------------------
    # Application for Recruiter B's job
    # ---------------------------------------------------------
    application_b = Application(
        candidate_id=candidate_profile.id,
        job_id=job_b.id,
        status=ApplicationStatus.APPLIED,
    )

    db.add_all([
        application_a,
        application_b,
    ])
    db.commit()

    db.refresh(application_a)
    db.refresh(application_b)

    # ---------------------------------------------------------
    # Generate JWTs
    # ---------------------------------------------------------
    recruiter_a_token = create_access_token(
        user_id=str(recruiter_a.id),
        role=recruiter_a.role.value,
    )

    recruiter_b_token = create_access_token(
        user_id=str(recruiter_b.id),
        role=recruiter_b.role.value,
    )

    candidate_token = create_access_token(
        user_id=str(candidate.id),
        role=candidate.role.value,
    )

    def auth_header(token: str) -> dict:
        return {
            "Authorization": f"Bearer {token}",
        }

    # ---------------------------------------------------------
    # Recruiter A → Update own application
    # Expected: 200
    # ---------------------------------------------------------
    response = client.patch(
        f"/applications/{application_a.id}/status",
        headers=auth_header(recruiter_a_token),
        json={
            "status": "shortlisted",
        },
    )

    print(
        "Recruiter A → Update own application:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(application_a.id)
    assert data["status"] == "shortlisted"

    print("Own application status update passed.")

    # ---------------------------------------------------------
    # Verify database value
    # ---------------------------------------------------------
    db.refresh(application_a)

    assert application_a.status == ApplicationStatus.SHORTLISTED

    print("Application status persisted successfully.")

    # ---------------------------------------------------------
    # Recruiter A → Update Recruiter B's application
    # Expected: 404
    # ---------------------------------------------------------
    response = client.patch(
        f"/applications/{application_b.id}/status",
        headers=auth_header(recruiter_a_token),
        json={
            "status": "interview",
        },
    )

    print(
        "Recruiter A → Update Recruiter B application:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"

    print("Application ownership protection passed.")

    # ---------------------------------------------------------
    # Recruiter B → Update own application
    # Expected: 200
    # ---------------------------------------------------------
    response = client.patch(
        f"/applications/{application_b.id}/status",
        headers=auth_header(recruiter_b_token),
        json={
            "status": "interview",
        },
    )

    print(
        "Recruiter B → Update own application:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(application_b.id)
    assert data["status"] == "interview"

    print("Recruiter B status update passed.")

    # ---------------------------------------------------------
    # Candidate → Update application status
    # Expected: 403
    # ---------------------------------------------------------
    response = client.patch(
        f"/applications/{application_a.id}/status",
        headers=auth_header(candidate_token),
        json={
            "status": "hired",
        },
    )

    print(
        "Candidate → Update application status:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 403

    print("Application status RBAC passed.")

    # ---------------------------------------------------------
    # Invalid status
    # Expected: 422
    # ---------------------------------------------------------
    response = client.patch(
        f"/applications/{application_a.id}/status",
        headers=auth_header(recruiter_a_token),
        json={
            "status": "invalid_status",
        },
    )

    print(
        "Invalid application status:",
        response.status_code,
    )
    print("Response:", response.json())

    assert response.status_code == 422

    print("Application status validation passed.")

    print("All application status tests passed.")

finally:
    # ---------------------------------------------------------
    # Cleanup
    # ---------------------------------------------------------
    if application_a:
        db.delete(application_a)

    if application_b:
        db.delete(application_b)

    if job_a:
        db.delete(job_a)

    if job_b:
        db.delete(job_b)

    if candidate_profile:
        db.delete(candidate_profile)

    if recruiter_a_profile:
        db.delete(recruiter_a_profile)

    if recruiter_b_profile:
        db.delete(recruiter_b_profile)

    if candidate:
        db.delete(candidate)

    if recruiter_a:
        db.delete(recruiter_a)

    if recruiter_b:
        db.delete(recruiter_b)

    db.commit()
    db.close()

    print("Temporary application status test data cleaned up.")