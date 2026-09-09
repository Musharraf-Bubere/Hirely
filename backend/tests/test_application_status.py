from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.models.application import Application, ApplicationStatus
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole
from app.core.security import hash_password, create_access_token


client = TestClient(app)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_user(db, role: UserRole):
    user = User(
        email=f"{role.value}-{uuid4()}@example.com",
        password_hash=hash_password("TestPassword123!"),
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_candidate(db, user):
    candidate = Candidate(
        user_id=user.id,
        first_name="Test",
        last_name="Candidate",
        headline="Python Developer",
        bio="Application status test candidate.",
        location="India",
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


def create_recruiter(db, user):
    recruiter = Recruiter(
        user_id=user.id,
        first_name="Test",
        last_name="Recruiter",
        job_title="Technical Recruiter",
        location="India",
    )

    db.add(recruiter)
    db.commit()
    db.refresh(recruiter)

    return recruiter


def create_job(db, recruiter, is_active=True):
    job = Job(
        recruiter_id=recruiter.id,
        title="Python Backend Developer",
        description=(
            "Build scalable backend services using Python and FastAPI."
        ),
        location="Remote",
        employment_type="FULL_TIME",
        experience_level="MID",
        salary_min=800000,
        salary_max=1400000,
        is_active=is_active,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def create_application(db, candidate, job):
    application = Application(
        candidate_id=candidate.id,
        job_id=job.id,
        status=ApplicationStatus.APPLIED,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def token_for(user):
    return create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )


# ---------------------------------------------------------
# 1. Recruiter can update application status for own job
# ---------------------------------------------------------

def test_recruiter_can_update_application_status_for_own_job():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None
    application = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        application = create_application(
            db,
            candidate,
            job,
        )

        token = token_for(recruiter_user)

        response = client.patch(
            f"/applications/{application.id}/status",
            json={
                "status": "shortlisted",
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Recruiter update status:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == str(application.id)
        assert data["candidate_id"] == str(candidate.id)
        assert data["job_id"] == str(job.id)
        assert data["status"] == "shortlisted"

        db.refresh(application)

        assert application.status == ApplicationStatus.SHORTLISTED

    finally:
        if application:
            db.delete(application)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 2. Recruiter can move application to interview
# ---------------------------------------------------------

def test_recruiter_can_move_application_to_interview():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None
    application = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        application = create_application(
            db,
            candidate,
            job,
        )

        token = token_for(recruiter_user)

        response = client.patch(
            f"/applications/{application.id}/status",
            json={
                "status": "interview",
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Move to interview:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "interview"

        db.refresh(application)

        assert application.status == ApplicationStatus.INTERVIEW

    finally:
        if application:
            db.delete(application)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 3. Recruiter can hire candidate
# ---------------------------------------------------------

def test_recruiter_can_hire_candidate():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None
    application = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        application = create_application(
            db,
            candidate,
            job,
        )

        token = token_for(recruiter_user)

        response = client.patch(
            f"/applications/{application.id}/status",
            json={
                "status": "hired",
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Hire candidate:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "hired"

        db.refresh(application)

        assert application.status == ApplicationStatus.HIRED

    finally:
        if application:
            db.delete(application)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 4. Recruiter can reject application
# ---------------------------------------------------------

def test_recruiter_can_reject_application():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None
    application = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        application = create_application(
            db,
            candidate,
            job,
        )

        token = token_for(recruiter_user)

        response = client.patch(
            f"/applications/{application.id}/status",
            json={
                "status": "rejected",
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Reject application:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "rejected"

        db.refresh(application)

        assert application.status == ApplicationStatus.REJECTED

    finally:
        if application:
            db.delete(application)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 5. Candidate cannot update application status
# ---------------------------------------------------------

def test_candidate_cannot_update_application_status():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None
    application = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        application = create_application(
            db,
            candidate,
            job,
        )

        token = token_for(candidate_user)

        response = client.patch(
            f"/applications/{application.id}/status",
            json={
                "status": "shortlisted",
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Candidate update attempt:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 403

        db.refresh(application)

        assert application.status == ApplicationStatus.APPLIED

    finally:
        if application:
            db.delete(application)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 6. Unauthenticated request is rejected
# ---------------------------------------------------------

def test_application_status_update_requires_authentication():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None
    application = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        application = create_application(
            db,
            candidate,
            job,
        )

        response = client.patch(
            f"/applications/{application.id}/status",
            json={
                "status": "shortlisted",
            },
        )

        print(
            "Unauthenticated status update:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 401

    finally:
        if application:
            db.delete(application)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 7. Recruiter cannot update another recruiter's application
# ---------------------------------------------------------

def test_recruiter_cannot_update_application_for_another_recruiters_job():
    db = SessionLocal()

    recruiter_a_user = None
    recruiter_a = None

    recruiter_b_user = None
    recruiter_b = None

    candidate_user = None
    candidate = None

    job = None
    application = None

    try:
        # -------------------------------------------------
        # Recruiter A
        # -------------------------------------------------

        recruiter_a_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter_a = create_recruiter(
            db,
            recruiter_a_user,
        )

        # -------------------------------------------------
        # Recruiter B
        # -------------------------------------------------

        recruiter_b_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter_b = create_recruiter(
            db,
            recruiter_b_user,
        )

        # -------------------------------------------------
        # Candidate
        # -------------------------------------------------

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        # -------------------------------------------------
        # Job owned by Recruiter A
        # -------------------------------------------------

        job = create_job(
            db,
            recruiter_a,
        )

        application = create_application(
            db,
            candidate,
            job,
        )

        # -------------------------------------------------
        # Recruiter B attempts to modify it
        # -------------------------------------------------

        token = token_for(recruiter_b_user)

        response = client.patch(
            f"/applications/{application.id}/status",
            json={
                "status": "shortlisted",
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Cross-recruiter status update:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 404

        db.refresh(application)

        assert application.status == ApplicationStatus.APPLIED

    finally:
        if application:
            db.delete(application)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter_a:
            db.delete(recruiter_a)

        if recruiter_b:
            db.delete(recruiter_b)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_a_user:
            db.delete(recruiter_a_user)

        if recruiter_b_user:
            db.delete(recruiter_b_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 8. Nonexistent application is rejected
# ---------------------------------------------------------

def test_recruiter_cannot_update_nonexistent_application():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        token = token_for(recruiter_user)

        fake_application_id = uuid4()

        response = client.patch(
            f"/applications/{fake_application_id}/status",
            json={
                "status": "shortlisted",
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Nonexistent application:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 404

    finally:
        if recruiter:
            db.delete(recruiter)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 9. Invalid application status is rejected
# ---------------------------------------------------------

def test_application_status_update_rejects_invalid_status():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None
    application = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        application = create_application(
            db,
            candidate,
            job,
        )

        token = token_for(recruiter_user)

        response = client.patch(
            f"/applications/{application.id}/status",
            json={
                "status": "invalid_status",
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Invalid application status:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 422

        db.refresh(application)

        assert application.status == ApplicationStatus.APPLIED

    finally:
        if application:
            db.delete(application)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()