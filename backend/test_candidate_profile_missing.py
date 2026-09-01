from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.user import User, UserRole


client = TestClient(app)
db = SessionLocal()

user = None

email = f"candidate-no-profile-{uuid4()}@example.com"

try:
    # Create a candidate user WITHOUT a Candidate profile
    user = User(
        email=email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.CANDIDATE,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate access token
    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )

    response = client.get(
        "/candidate/profile",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate profile not found"

    print("Missing candidate profile test passed.")

finally:
    if user:
        db.delete(user)

    db.commit()
    db.close()

    print("Temporary candidate user cleaned up.")