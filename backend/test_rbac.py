from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.user import User, UserRole


client = TestClient(app)
db = SessionLocal()

candidate = None
recruiter = None

candidate_email = f"rbac-candidate-{uuid4()}@example.com"
recruiter_email = f"rbac-recruiter-{uuid4()}@example.com"

try:
    # ---------------------------------------------------------
    # Create temporary candidate
    # ---------------------------------------------------------
    candidate = User(
        email=candidate_email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.CANDIDATE,
    )

    # ---------------------------------------------------------
    # Create temporary recruiter
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
    # Generate JWTs
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
    # Candidate → Candidate profile
    # Expected: 200
    # ---------------------------------------------------------
    response = client.get(
        "/candidate/profile",
        headers=auth_header(candidate_token),
    )

    print(
        "Candidate → Candidate profile:",
        response.status_code,
    )
    assert response.status_code == 200

    # ---------------------------------------------------------
    # Candidate → Recruiter profile
    # Expected: 403
    # ---------------------------------------------------------
    response = client.get(
        "/recruiter/profile",
        headers=auth_header(candidate_token),
    )

    print(
        "Candidate → Recruiter profile:",
        response.status_code,
    )
    assert response.status_code == 403

    # ---------------------------------------------------------
    # Recruiter → Recruiter profile
    # Expected: 200
    # ---------------------------------------------------------
    response = client.get(
        "/recruiter/profile",
        headers=auth_header(recruiter_token),
    )

    print(
        "Recruiter → Recruiter profile:",
        response.status_code,
    )
    assert response.status_code == 200

    # ---------------------------------------------------------
    # Recruiter → Candidate profile
    # Expected: 403
    # ---------------------------------------------------------
    response = client.get(
        "/candidate/profile",
        headers=auth_header(recruiter_token),
    )

    print(
        "Recruiter → Candidate profile:",
        response.status_code,
    )
    assert response.status_code == 403

    print("All RBAC tests passed.")

finally:
    # ---------------------------------------------------------
    # Cleanup temporary users
    # ---------------------------------------------------------
    if candidate:
        db.delete(candidate)

    if recruiter:
        db.delete(recruiter)

    db.commit()
    db.close()

    print("Temporary RBAC test users cleaned up.")