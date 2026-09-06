from io import BytesIO
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User, UserRole


client = TestClient(app)


def test_candidate_can_upload_resume():
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    email = f"resume-api-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary candidate user
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
        # Create candidate profile
        # ---------------------------------------------------------
        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
            headline="AI Engineer",
            bio="Resume API integration test.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Create test resume file
        # ---------------------------------------------------------
        resume_content = b"%PDF-1.4 test resume content"

        # ---------------------------------------------------------
        # Upload resume
        # Expected: 200
        # ---------------------------------------------------------
        response = client.post(
            "/resumes",
            headers={
                "Authorization": f"Bearer {token}",
            },
            files={
                "resume": (
                    "test_resume.pdf",
                    BytesIO(resume_content),
                    "application/pdf",
                ),
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 200

        data = response.json()

        assert data["filename"] == "test_resume.pdf"
        assert data["content_type"] == "application/pdf"
        assert data["file_path"]

        # ---------------------------------------------------------
        # Verify Resume database record
        # ---------------------------------------------------------
        resume = (
            db.query(Resume)
            .filter(
                Resume.candidate_id == candidate.id,
                Resume.original_filename == "test_resume.pdf",
            )
            .first()
        )

        assert resume is not None
        assert resume.file_path == data["file_path"]
        assert resume.parsing_status == "PENDING"
        assert resume.is_active is False

        print("Resume upload API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary resume API data cleaned up.")

def test_unauthenticated_user_cannot_upload_resume():
    response = client.post(
        "/resumes",
        files={
            "resume": (
                "test_resume.pdf",
                BytesIO(b"%PDF-1.4 test resume content"),
                "application/pdf",
            ),
        },
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

    print("Unauthenticated resume upload test passed.")


def test_candidate_without_profile_cannot_upload_resume():
    db = SessionLocal()

    user = None

    email = f"resume-no-profile-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create candidate user WITHOUT a Candidate profile
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
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Attempt resume upload
        # Expected: 404
        # ---------------------------------------------------------
        response = client.post(
            "/resumes",
            headers={
                "Authorization": f"Bearer {token}",
            },
            files={
                "resume": (
                    "test_resume.pdf",
                    BytesIO(b"%PDF-1.4 test resume content"),
                    "application/pdf",
                ),
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 404
        assert response.json()["detail"] == "Candidate profile not found"

        print("Candidate without profile test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary user data cleaned up.")

def test_candidate_cannot_upload_invalid_resume_type():
    db = SessionLocal()

    user = None
    candidate = None

    email = f"resume-invalid-type-{uuid4()}@example.com"

    try:
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
            headline="AI Engineer",
            bio="Invalid resume type test.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        response = client.post(
            "/resumes",
            headers={
                "Authorization": f"Bearer {token}",
            },
            files={
                "resume": (
                    "malicious.exe",
                    BytesIO(b"fake executable content"),
                    "application/octet-stream",
                ),
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Only PDF and DOCX resume files are allowed"
        )

        print("Invalid resume type test passed.")

    finally:
        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

def test_candidate_cannot_upload_oversized_resume():
    db = SessionLocal()

    user = None
    candidate = None

    email = f"resume-oversized-{uuid4()}@example.com"

    try:
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
            headline="AI Engineer",
            bio="Oversized resume test.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # 10 MB + 1 byte
        oversized_content = b"x" * (10 * 1024 * 1024 + 1)

        response = client.post(
            "/resumes",
            headers={
                "Authorization": f"Bearer {token}",
            },
            files={
                "resume": (
                    "oversized_resume.pdf",
                    BytesIO(oversized_content),
                    "application/pdf",
                ),
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Resume file size must not exceed 10 MB"
        )

        print("Oversized resume test passed.")

    finally:
        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

def test_candidate_can_list_own_resumes():
    db = SessionLocal()

    user = None
    candidate = None
    resume_one = None
    resume_two = None

    email = f"resume-list-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary candidate user
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
        # Create candidate profile
        # ---------------------------------------------------------
        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
            headline="AI Engineer",
            bio="Resume list API integration test.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create two resume versions
        # ---------------------------------------------------------
        resume_one = Resume(
            candidate_id=candidate.id,
            original_filename="older_resume.pdf",
            file_path="test_data/older_resume.pdf",
            parsing_status="COMPLETED",
            is_active=False,
        )

        db.add(resume_one)
        db.commit()
        db.refresh(resume_one)

        resume_two = Resume(
            candidate_id=candidate.id,
            original_filename="newer_resume.pdf",
            file_path="test_data/newer_resume.pdf",
            parsing_status="PENDING",
            is_active=True,
        )

        db.add(resume_two)
        db.commit()
        db.refresh(resume_two)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Get resumes
        # Expected: 200
        # ---------------------------------------------------------
        response = client.get(
            "/resumes",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2

        # Newest resume should come first
        assert data[0]["id"] == str(resume_two.id)
        assert data[0]["original_filename"] == "newer_resume.pdf"
        assert data[0]["parsing_status"] == "PENDING"
        assert data[0]["is_active"] is True

        assert data[1]["id"] == str(resume_one.id)
        assert data[1]["original_filename"] == "older_resume.pdf"
        assert data[1]["parsing_status"] == "COMPLETED"
        assert data[1]["is_active"] is False

        # Internal fields must not be exposed
        assert "candidate_id" not in data[0]
        assert "file_path" not in data[0]
        assert "parsed_data" not in data[0]

        print("Resume list API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if resume_two:
            db.delete(resume_two)

        if resume_one:
            db.delete(resume_one)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()