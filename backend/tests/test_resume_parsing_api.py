from uuid import uuid4

from fastapi.testclient import TestClient

from app.ai.parsers.schemas import ResumeData
from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.candidate_skill import CandidateSkill
from app.models.resume import Resume
from app.models.user import User, UserRole


client = TestClient(app)


class FakeResumeParserService:
    def parse_file(self, file_path):
        return ResumeData(
            name="Test Candidate",
            email="test@example.com",
            skills=["Python", "SQL"],
        )


def test_candidate_can_parse_resume(monkeypatch):
    db = SessionLocal()

    user = None
    candidate = None
    resume = None

    email = f"resume-parse-api-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create candidate user
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
            bio="Resume parsing API integration test.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create resume record
        # ---------------------------------------------------------
        resume = Resume(
            candidate_id=candidate.id,
            original_filename="test_resume.pdf",
            file_path="test_data/test_resume.pdf",
            parsing_status="PENDING",
            is_active=False,
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # ---------------------------------------------------------
        # Replace real parser with fake parser
        # ---------------------------------------------------------
        monkeypatch.setattr(
            "app.api.resumes.ResumeParserService",
            FakeResumeParserService,
        )

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Parse resume
        # ---------------------------------------------------------
        response = client.post(
            f"/resumes/{resume.id}/parse",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # Verify API response
        # ---------------------------------------------------------
        assert response.status_code == 200

        data = response.json()

        assert data["id"] == str(resume.id)
        assert data["original_filename"] == "test_resume.pdf"
        assert data["parsing_status"] == "COMPLETED"
        assert data["is_active"] is False

        # ---------------------------------------------------------
        # Verify database state
        # ---------------------------------------------------------
        db.refresh(resume)

        assert resume.parsing_status == "COMPLETED"
        assert resume.parsed_data is not None

        assert resume.parsed_data == {
            "name": "Test Candidate",
            "email": "test@example.com",
            "phone": None,
            "location": None,
            "headline": None,
            "summary": None,
            "skills": ["Python", "SQL"],
            "experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
        }

        # ---------------------------------------------------------
        # Internal fields must not be exposed
        # ---------------------------------------------------------
        assert "candidate_id" not in data
        assert "file_path" not in data
        assert "parsed_data" not in data

        print("Resume parsing API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup resume
        # ---------------------------------------------------------
        if resume:
            db.delete(resume)

        # ---------------------------------------------------------
        # Cleanup candidate skill associations first
        # ---------------------------------------------------------
        if candidate:
            db.query(CandidateSkill).filter(
                CandidateSkill.candidate_id == candidate.id
            ).delete(
                synchronize_session=False,
            )

        # Flush association deletions before deleting candidate
        db.flush()

        # ---------------------------------------------------------
        # Cleanup candidate
        # ---------------------------------------------------------
        if candidate:
            db.delete(candidate)

        # ---------------------------------------------------------
        # Cleanup user
        # ---------------------------------------------------------
        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_candidate_cannot_parse_nonexistent_resume():
    db = SessionLocal()

    user = None
    candidate = None

    email = f"resume-parse-not-found-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create candidate user
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
            bio="Resume parsing not found test.",
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
        # Generate fake resume ID
        # ---------------------------------------------------------
        fake_resume_id = uuid4()

        # ---------------------------------------------------------
        # Attempt to parse nonexistent resume
        # ---------------------------------------------------------
        response = client.post(
            f"/resumes/{fake_resume_id}/parse",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 404
        assert response.json()["detail"] == "Resume not found"

    finally:
        # ---------------------------------------------------------
        # Cleanup candidate skill associations
        # ---------------------------------------------------------
        if candidate:
            db.query(CandidateSkill).filter(
                CandidateSkill.candidate_id == candidate.id
            ).delete(
                synchronize_session=False,
            )

        db.flush()

        # ---------------------------------------------------------
        # Cleanup candidate
        # ---------------------------------------------------------
        if candidate:
            db.delete(candidate)

        # ---------------------------------------------------------
        # Cleanup user
        # ---------------------------------------------------------
        if user:
            db.delete(user)

        db.commit()
        db.close()


def test_candidate_cannot_parse_another_candidates_resume():
    db = SessionLocal()

    user_one = None
    candidate_one = None

    user_two = None
    candidate_two = None

    resume = None

    email_one = f"resume-parse-owner-{uuid4()}@example.com"
    email_two = f"resume-parse-attacker-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Candidate 1 - Resume owner
        # ---------------------------------------------------------
        user_one = User(
            email=email_one,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user_one)
        db.commit()
        db.refresh(user_one)

        candidate_one = Candidate(
            user_id=user_one.id,
            first_name="Resume",
            last_name="Owner",
            headline="AI Engineer",
            bio="Resume owner.",
            location="India",
        )

        db.add(candidate_one)
        db.commit()
        db.refresh(candidate_one)

        # ---------------------------------------------------------
        # Candidate 2 - Attacker
        # ---------------------------------------------------------
        user_two = User(
            email=email_two,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user_two)
        db.commit()
        db.refresh(user_two)

        candidate_two = Candidate(
            user_id=user_two.id,
            first_name="Resume",
            last_name="Attacker",
            headline="AI Engineer",
            bio="Another candidate.",
            location="India",
        )

        db.add(candidate_two)
        db.commit()
        db.refresh(candidate_two)

        # ---------------------------------------------------------
        # Resume belongs to Candidate 1
        # ---------------------------------------------------------
        resume = Resume(
            candidate_id=candidate_one.id,
            original_filename="private_resume.pdf",
            file_path="test_data/private_resume.pdf",
            parsing_status="PENDING",
            is_active=False,
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # ---------------------------------------------------------
        # Token for Candidate 2
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user_two.id),
            role=user_two.role.value,
        )

        # ---------------------------------------------------------
        # Candidate 2 attempts to parse Candidate 1's resume
        # ---------------------------------------------------------
        response = client.post(
            f"/resumes/{resume.id}/parse",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 404
        assert response.json()["detail"] == "Resume not found"

        # ---------------------------------------------------------
        # Verify resume was not modified
        # ---------------------------------------------------------
        db.refresh(resume)

        assert resume.parsing_status == "PENDING"
        assert resume.parsed_data is None

    finally:
        # ---------------------------------------------------------
        # Cleanup resume
        # ---------------------------------------------------------
        if resume:
            db.delete(resume)

        # ---------------------------------------------------------
        # Cleanup Candidate 1 skill associations
        # ---------------------------------------------------------
        if candidate_one:
            db.query(CandidateSkill).filter(
                CandidateSkill.candidate_id == candidate_one.id
            ).delete(
                synchronize_session=False,
            )

        # ---------------------------------------------------------
        # Cleanup Candidate 2 skill associations
        # ---------------------------------------------------------
        if candidate_two:
            db.query(CandidateSkill).filter(
                CandidateSkill.candidate_id == candidate_two.id
            ).delete(
                synchronize_session=False,
            )

        db.flush()

        # ---------------------------------------------------------
        # Cleanup candidates
        # ---------------------------------------------------------
        if candidate_one:
            db.delete(candidate_one)

        if candidate_two:
            db.delete(candidate_two)

        # ---------------------------------------------------------
        # Cleanup users
        # ---------------------------------------------------------
        if user_one:
            db.delete(user_one)

        if user_two:
            db.delete(user_two)

        db.commit()
        db.close()


def test_unauthenticated_user_cannot_parse_resume():
    fake_resume_id = uuid4()

    response = client.post(
        f"/resumes/{fake_resume_id}/parse",
    )

    print("Status:", response.status_code)
    print("Response:", response.json())

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"