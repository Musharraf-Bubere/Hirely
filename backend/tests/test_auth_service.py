from uuid import uuid4

from app.core.security import verify_password
from app.db.session import SessionLocal
from app.models import Candidate, Recruiter, User
from app.schemas.auth import RegisterRequest
from app.services.auth import authenticate_user, register_user


def test_auth_service_candidate_registration_and_authentication():
    db = SessionLocal()

    test_email = f"auth-candidate-{uuid4()}@example.com"

    try:
        data = RegisterRequest(
            first_name="Test",
            last_name="Candidate",
            email=test_email,
            password="secret123",
            role="candidate",
        )

        user = register_user(db, data)

        print("Candidate User ID:", user.id)
        print("Email:", user.email)
        print("Role:", user.role)

        assert user.email == test_email
        assert user.role.value == "candidate"
        assert user.password_hash != "secret123"
        assert verify_password("secret123", user.password_hash) is True

        candidate = (
            db.query(Candidate)
            .filter(Candidate.user_id == user.id)
            .first()
        )

        assert candidate is not None
        assert candidate.first_name == "Test"
        assert candidate.last_name == "Candidate"

        recruiter = (
            db.query(Recruiter)
            .filter(Recruiter.user_id == user.id)
            .first()
        )

        assert recruiter is None

        authenticated_user = authenticate_user(
            db,
            test_email,
            "secret123",
        )

        assert authenticated_user is not None
        assert authenticated_user.id == user.id

        wrong_password_user = authenticate_user(
            db,
            test_email,
            "wrong-password",
        )

        assert wrong_password_user is None

        nonexistent_user = authenticate_user(
            db,
            "does-not-exist@example.com",
            "secret123",
        )

        assert nonexistent_user is None

    finally:
        candidate = (
            db.query(Candidate)
            .filter(Candidate.user_id == user.id)
            .first()
            if "user" in locals()
            else None
        )

        if candidate:
            db.delete(candidate)

        user = (
            db.query(User)
            .filter(User.email == test_email)
            .first()
        )

        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_auth_service_recruiter_registration():
    db = SessionLocal()

    test_email = f"auth-recruiter-{uuid4()}@example.com"

    try:
        data = RegisterRequest(
            first_name="Test",
            last_name="Recruiter",
            email=test_email,
            password="secret123",
            role="recruiter",
        )

        user = register_user(db, data)

        print("Recruiter User ID:", user.id)
        print("Email:", user.email)
        print("Role:", user.role)

        assert user.email == test_email
        assert user.role.value == "recruiter"
        assert user.password_hash != "secret123"
        assert verify_password("secret123", user.password_hash) is True

        recruiter = (
            db.query(Recruiter)
            .filter(Recruiter.user_id == user.id)
            .first()
        )

        assert recruiter is not None
        assert recruiter.first_name == "Test"
        assert recruiter.last_name == "Recruiter"
        assert recruiter.company_id is None
        assert recruiter.job_title is None
        assert recruiter.location is None

        candidate = (
            db.query(Candidate)
            .filter(Candidate.user_id == user.id)
            .first()
        )

        assert candidate is None

    finally:
        recruiter = (
            db.query(Recruiter)
            .filter(Recruiter.user_id == user.id)
            .first()
            if "user" in locals()
            else None
        )

        if recruiter:
            db.delete(recruiter)

        user = (
            db.query(User)
            .filter(User.email == test_email)
            .first()
        )

        if user:
            db.delete(user)

        db.commit()
        db.close()