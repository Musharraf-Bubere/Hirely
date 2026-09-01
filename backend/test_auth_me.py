from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.user import User, UserRole


client = TestClient(app)
db = SessionLocal()

user = None

email = f"auth-me-{uuid4()}@example.com"

try:
    # ---------------------------------------------------------
    # Create temporary user
    # ---------------------------------------------------------
    user = User(
        email=email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.CANDIDATE,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # ---------------------------------------------------------
    # Generate valid JWT
    # ---------------------------------------------------------
    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )

    # ---------------------------------------------------------
    # Valid token → /auth/me
    # Expected: 200
    # ---------------------------------------------------------
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    print("Valid token → /auth/me:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(user.id)
    assert data["email"] == email
    assert data["role"] == "candidate"
    assert data["is_active"] is True

    # ---------------------------------------------------------
    # No token → /auth/me
    # Expected: 401
    # ---------------------------------------------------------
    response = client.get("/auth/me")

    print("No token → /auth/me:", response.status_code)

    assert response.status_code == 401

    # ---------------------------------------------------------
    # Invalid token → /auth/me
    # Expected: 401
    # ---------------------------------------------------------
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    print("Invalid token → /auth/me:", response.status_code)

    assert response.status_code == 401

    print("Auth /me tests passed.")

finally:
    if user:
        db.delete(user)

    db.commit()
    db.close()

    print("Temporary auth/me test user cleaned up.")