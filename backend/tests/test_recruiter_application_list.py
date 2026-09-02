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


def test_recruiter_application_list_returns_only_owned_applications():
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

    candidate_email = f"recruiter-list-candidate-{uuid4()}@example.com"
    recruiter_a_email = f"recruiter-a-{uuid4()}@example.com"
    recruiter_b_email = f"recruiter-b-{uuid4()}@example.com"

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
            first_name="Test",
            last_name="Candidate",
            headline="Python Developer",
            bio="Recruiter application listing test candidate.",
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
        # Recruiter A's job
        # ---------------------------------------------------------
        job_a = Job(
            recruiter_id=recruiter_a_profile.id,
            title="Python Backend Developer",
            description="Recruiter A test job.",
            location="Remote",
            employment_type="full_time",
            experience_level="mid",
            salary_min=800000,
            salary_max=1400000,
        )

        # ---------------------------------------------------------
        # Recruiter B's job
        # ---------------------------------------------------------
        job_b = Job(
            recruiter_id=recruiter_b_profile.id,
            title="Data Engineer",
            description="Recruiter B test job.",
            location="Remote",
            employment_type="full_time",
            experience_level="mid",
            salary_min=900000,
            salary_max=1500000,
        )

        db.add_all([job_a, job_b])
        db.commit()

        db.refresh(job_a)
        db.refresh(job_b)

        # ---------------------------------------------------------
        # Application to Recruiter A's job
        # ---------------------------------------------------------
        application_a = Application(
            candidate_id=candidate_profile.id,
            job_id=job_a.id,
        )

        # ---------------------------------------------------------
        # Application to Recruiter B's job
        # ---------------------------------------------------------
        application_b = Application(
            candidate_id=candidate_profile.id,
            job_id=job_b.id,
        )

        db.add_all([
            application_a,
            application_b,
        ])
        db.commit()

        db.refresh(application_a)
        db.refresh(application_b)

        # ---------------------------------------------------------
        # Generate recruiter tokens
        # ---------------------------------------------------------
        recruiter_a_token = create_access_token(
            user_id=str(recruiter_a.id),
            role=recruiter_a.role.value,
        )

        recruiter_b_token = create_access_token(
            user_id=str(recruiter_b.id),
            role=recruiter_b.role.value,
        )

        def auth_header(token: str) -> dict:
            return {
                "Authorization": f"Bearer {token}",
            }

        # ---------------------------------------------------------
        # Recruiter A → own applications
        # Expected: 200
        # Expected: only application A
        # ---------------------------------------------------------
        response = client.get(
            "/applications/recruiter",
            headers=auth_header(recruiter_a_token),
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == str(application_a.id)
        assert data[0]["job_id"] == str(job_a.id)

        # ---------------------------------------------------------
        # Recruiter B → own applications
        # Expected: 200
        # Expected: only application B
        # ---------------------------------------------------------
        response = client.get(
            "/applications/recruiter",
            headers=auth_header(recruiter_b_token),
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == str(application_b.id)
        assert data[0]["job_id"] == str(job_b.id)

        # ---------------------------------------------------------
        # Candidate → recruiter applications endpoint
        # Expected: 403
        # ---------------------------------------------------------
        candidate_token = create_access_token(
            user_id=str(candidate.id),
            role=candidate.role.value,
        )

        response = client.get(
            "/applications/recruiter",
            headers=auth_header(candidate_token),
        )

        assert response.status_code == 403

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