from uuid import uuid4

from fastapi.testclient import TestClient

from app.ai.career_coach.schemas import CareerCoachResponse
from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.user import User, UserRole


client = TestClient(app)


def create_test_candidate():
    """
    Create a temporary candidate and return:
    database session, user, candidate, and JWT token.
    """
    db = SessionLocal()

    email = f"career-coach-validation-{uuid4()}@example.com"

    user = User(
        email=email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.CANDIDATE,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    candidate = Candidate(
        user_id=user.id,
        first_name="Test",
        last_name="Candidate",
        headline="Python Developer",
        bio="Career Coach API validation test candidate.",
        location="India",
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )

    return db, user, candidate, token


def cleanup_test_candidate(db, user, candidate):
    """
    Remove temporary candidate test data.
    """
    if candidate:
        db.delete(candidate)

    if user:
        db.delete(user)

    db.commit()
    db.close()


def test_career_coach_rejects_empty_message():
    db, user, candidate, token = create_test_candidate()

    try:
        response = client.post(
            "/candidate/career-coach",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "message": "",
            },
        )

        print("Empty message:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 422

        print("Empty message validation test passed.")

    finally:
        cleanup_test_candidate(db, user, candidate)
        print("Temporary empty-message test data cleaned up.")


def test_career_coach_rejects_whitespace_only_message():
    db, user, candidate, token = create_test_candidate()

    try:
        response = client.post(
            "/candidate/career-coach",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "message": "   ",
            },
        )

        print("Whitespace message:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 422

        print("Whitespace message validation test passed.")

    finally:
        cleanup_test_candidate(db, user, candidate)
        print("Temporary whitespace test data cleaned up.")


def test_career_coach_rejects_message_over_4000_characters():
    db, user, candidate, token = create_test_candidate()

    try:
        message = "a" * 4001

        response = client.post(
            "/candidate/career-coach",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "message": message,
            },
        )

        print("Over-limit message:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 422

        print("4000-character limit validation test passed.")

    finally:
        cleanup_test_candidate(db, user, candidate)
        print("Temporary over-limit test data cleaned up.")


def test_career_coach_accepts_valid_message(monkeypatch):
    db, user, candidate, token = create_test_candidate()

    from app.api import candidate as candidate_api

    expected_response = CareerCoachResponse(
        answer=(
            "Focus on strengthening your machine learning fundamentals."
        ),
        recommendations=[
            "Build one practical ML project.",
        ],
        skills_to_improve=[
            "Machine Learning",
        ],
        next_steps=[
            "Complete an end-to-end ML project.",
        ],
    )

    def mock_generate_response(db, candidate, request):
        return expected_response

    monkeypatch.setattr(
        candidate_api.career_coach_service,
        "generate_response",
        mock_generate_response,
    )

    try:
        response = client.post(
            "/candidate/career-coach",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "message": (
                    "What should I learn to become better "
                    "at machine learning?"
                ),
            },
        )

        print("Valid message:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 200
        assert response.json() == expected_response.model_dump()

        print("Valid message test passed.")

    finally:
        cleanup_test_candidate(db, user, candidate)
        print("Temporary valid-message test data cleaned up.")