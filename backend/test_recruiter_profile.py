from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.company import Company
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)
db = SessionLocal()

user = None
recruiter = None
company = None

email = f"recruiter-profile-{uuid4()}@example.com"

try:
    # Create temporary recruiter user
    user = User(
        email=email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.RECRUITER,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create company
    company = Company(
        name="Hirely Test Company",
        description="Recruiter profile integration test company.",
        website="https://hirely.example.com",
        industry="Technology",
        location="India",
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    # Create recruiter linked to user and company
    recruiter = Recruiter(
        user_id=user.id,
        company_id=company.id,
        first_name="Test",
        last_name="Recruiter",
        job_title="Talent Acquisition Specialist",
        location="India",
    )

    db.add(recruiter)
    db.commit()
    db.refresh(recruiter)

    # Generate access token
    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )

    response = client.get(
        "/recruiter/profile",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 200

    data = response.json()

    # User data
    assert data["id"] == str(user.id)
    assert data["email"] == email
    assert data["role"] == "recruiter"
    assert data["is_active"] is True

    # Recruiter data
    assert data["first_name"] == "Test"
    assert data["last_name"] == "Recruiter"
    assert data["job_title"] == "Talent Acquisition Specialist"
    assert data["location"] == "India"

    # Company data
    assert data["company"] is not None
    assert data["company"]["id"] == str(company.id)
    assert data["company"]["name"] == "Hirely Test Company"
    assert (
        data["company"]["description"]
        == "Recruiter profile integration test company."
    )
    assert data["company"]["website"] == "https://hirely.example.com"
    assert data["company"]["industry"] == "Technology"
    assert data["company"]["location"] == "India"

    print("Recruiter profile test passed.")

finally:
    if recruiter:
        db.delete(recruiter)

    if company:
        db.delete(company)

    if user:
        db.delete(user)

    db.commit()
    db.close()

    print("Temporary recruiter profile data cleaned up.")