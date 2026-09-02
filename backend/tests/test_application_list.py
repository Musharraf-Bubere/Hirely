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


def test_candidate_can_list_own_applications_and_recruiter_cannot():
    db = SessionLocal()

    candidate = None
    candidate_profile = None
    recruiter = None
    recruiter_profile = None
    job = None
    application = None

    candidate_email = f"application-list-candidate-{uuid4()}@example.com"
    recruiter_email = f"application-list-recruiter-{uuid4()}@example.com"

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
            first_name="Application",
            last_name="Candidate",
            headline="Python Developer",
            bio="Application listing test candidate.",
            location="India",
        )

        # ---------------------------------------------------------
        # Create recruiter profile
        # ---------------------------------------------------------
        recruiter_profile = Recruiter(
            user_id=recruiter.id,
            first_name="Application",
            last_name="Recruiter",
            job_title="Talent Acquisition Specialist",
            location="India",
        )

        db.add_all([candidate_profile, recruiter_profile])
        db.commit()

        db.refresh(candidate_profile)
        db.refresh(recruiter_profile)

        # ---------------------------------------------------------
        # Create job
        # ---------------------------------------------------------
        job = Job(
            recruiter_id=recruiter_profile.id,
            title="Python Backend Developer",
            description="Application listing test job.",
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
        # Create application directly
        # ---------------------------------------------------------
        application = Application(
            candidate_id=candidate_profile.id,
            job_id=job.id,
        )

        db.add(application)
        db.commit()

        db.refresh(application)

        # ---------------------------------------------------------
        # Generate tokens
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
        # Candidate → Own applications
        # Expected: 200
        # ---------------------------------------------------------
        response = client.get(
            "/applications/me",
            headers=auth_header(candidate_token),
        )

        print(
            "Candidate → GET /applications/me:",
            response.status_code,
        )
        print("Response:", response.json())

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == str(application.id)
        assert data[0]["candidate_id"] == str(candidate_profile.id)
        assert data[0]["job_id"] == str(job.id)
        assert data[0]["status"] == "applied"

        print("Candidate application listing passed.")

        # ---------------------------------------------------------
        # Recruiter → Candidate application listing
        # Expected: 403
        # ---------------------------------------------------------
        response = client.get(
            "/applications/me",
            headers=auth_header(recruiter_token),
        )

        print(
            "Recruiter → GET /applications/me:",
            response.status_code,
        )
        print("Response:", response.json())

        assert response.status_code == 403

        print("Application listing RBAC passed.")

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

        print("Temporary application listing test data cleaned up.")