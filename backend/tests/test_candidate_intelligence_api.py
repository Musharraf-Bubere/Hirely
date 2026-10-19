from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

from app.ai.candidate_intelligence.schemas import (
    CandidateApplicationInfo,
    CandidateIntelligenceItem,
    CandidateIntelligenceResponse,
    CandidateProfileSummary,
)
from app.ai.matching.explanation import MatchExplanation, MatchExplanationEvidence
from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)


# =====================================================================
# Fixtures and Helpers
# =====================================================================

def create_test_recruiter(db, *, suffix: str = ""):
    email = f"ci-rec-{suffix}-{uuid4()}@example.com"
    user = User(
        email=email,
        password_hash=hash_password("RecruiterPass123!"),
        role=UserRole.RECRUITER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    recruiter = Recruiter(
        user_id=user.id,
        first_name="Talent",
        last_name=f"Lead{suffix}",
        job_title="Director of Talent",
        location="Bengaluru",
    )
    db.add(recruiter)
    db.commit()
    db.refresh(recruiter)

    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )
    return user, recruiter, token


def create_test_candidate(db):
    email = f"ci-cand-{uuid4()}@example.com"
    user = User(
        email=email,
        password_hash=hash_password("CandidatePass123!"),
        role=UserRole.CANDIDATE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    candidate = Candidate(
        user_id=user.id,
        first_name="Candidate",
        last_name="Applicant",
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )
    return user, candidate, token


def create_test_job(db, recruiter, *, is_active=True):
    job = Job(
        recruiter_id=recruiter.id,
        title="Senior Python Backend Engineer",
        description="Design and build high-throughput APIs using Python, FastAPI, and Docker.",
        location="Bengaluru",
        employment_type="Full-time",
        experience_level="Senior",
        salary_min=1800000,
        salary_max=2800000,
        is_active=is_active,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def make_mock_intelligence_response(job_id: uuid4, job_title: str) -> CandidateIntelligenceResponse:
    cand_id = uuid4()
    item = CandidateIntelligenceItem(
        rank=1,
        candidate=CandidateProfileSummary(
            id=cand_id,
            first_name="Ananya",
            last_name="Sharma",
            full_name="Ananya Sharma",
            headline="Senior Backend Engineer",
            location="Bengaluru",
            bio="Building cloud architectures.",
            skills=["Python", "FastAPI", "Docker"],
            experience=[],
            education=[],
        ),
        application=CandidateApplicationInfo(
            application_id=uuid4(),
            status="applied",
        ),
        overall_score=0.91,
        required_skill_score=0.95,
        preferred_skill_score=0.85,
        semantic_similarity=0.90,
        required_matched=["Python", "FastAPI"],
        required_missing=[],
        preferred_matched=["Docker"],
        preferred_missing=[],
        explanation=MatchExplanation(
            summary="Candidate exhibits exceptional alignment with required backend tech stack.",
            strengths=["Deep Python expertise."],
            gaps=[],
            evidence=MatchExplanationEvidence(
                required_skill_score=0.95,
                preferred_skill_score=0.85,
                semantic_similarity=0.90,
            ),
            caveats=[],
        ),
    )

    return CandidateIntelligenceResponse(
        job_id=job_id,
        job_title=job_title,
        total_candidates=1,
        matched_count=1,
        results=[item],
        available_skills=["Docker", "FastAPI", "Python"],
    )


# =====================================================================
# API Tests
# =====================================================================

def test_candidate_intelligence_unauthenticated():
    response = client.post(f"/recruiter/jobs/{uuid4()}/candidate-intelligence")
    assert response.status_code in (401, 403)


def test_candidate_intelligence_candidate_forbidden():
    db = SessionLocal()
    user, candidate, token = create_test_candidate(db)
    try:
        response = client.post(
            f"/recruiter/jobs/{uuid4()}/candidate-intelligence",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
        assert "Insufficient permissions" in response.json()["detail"]
    finally:
        db.delete(candidate)
        db.delete(user)
        db.commit()
        db.close()


def test_candidate_intelligence_recruiter_profile_missing():
    db = SessionLocal()
    user = User(
        email=f"noprofile-ci-{uuid4()}@example.com",
        password_hash=hash_password("Pass123!"),
        role=UserRole.RECRUITER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )

    try:
        response = client.post(
            f"/recruiter/jobs/{uuid4()}/candidate-intelligence",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        assert "Recruiter profile not found" in response.json()["detail"]
    finally:
        db.delete(user)
        db.commit()
        db.close()


def test_candidate_intelligence_missing_job():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    missing_job_id = uuid4()
    try:
        response = client.post(
            f"/recruiter/jobs/{missing_job_id}/candidate-intelligence",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        assert "Job not found" in response.json()["detail"]
    finally:
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_candidate_intelligence_ownership_forbidden():
    """Recruiter A cannot view candidate intelligence for a job owned by Recruiter B."""
    db = SessionLocal()
    user_a, recruiter_a, token_a = create_test_recruiter(db, suffix="a")
    user_b, recruiter_b, _ = create_test_recruiter(db, suffix="b")
    job_b = create_test_job(db, recruiter_b)

    try:
        response = client.post(
            f"/recruiter/jobs/{job_b.id}/candidate-intelligence",
            headers={"Authorization": f"Bearer {token_a}"},
        )
        assert response.status_code == 403
        assert "permission to view" in response.json()["detail"].lower()
    finally:
        db.delete(job_b)
        db.delete(recruiter_a)
        db.delete(user_a)
        db.delete(recruiter_b)
        db.delete(user_b)
        db.commit()
        db.close()


def test_candidate_intelligence_inactive_job():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter, is_active=False)

    try:
        response = client.post(
            f"/recruiter/jobs/{job.id}/candidate-intelligence",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 400
        assert "inactive" in response.json()["detail"].lower()
    finally:
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_candidate_intelligence_success():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter)

    try:
        with patch("app.ai.candidate_intelligence.service.candidate_intelligence_service.get_candidate_intelligence") as mock_ci:
            mock_ci.return_value = make_mock_intelligence_response(job.id, job.title)

            response = client.post(
                f"/recruiter/jobs/{job.id}/candidate-intelligence",
                headers={"Authorization": f"Bearer {token}"},
                json={"query": "python", "min_score": 0.8},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == str(job.id)
            assert data["total_candidates"] == 1
            assert data["matched_count"] == 1
            assert len(data["results"]) == 1

            result = data["results"][0]
            assert result["candidate"]["full_name"] == "Ananya Sharma"
            assert result["overall_score"] == 0.91
            assert result["application"]["status"] == "applied"
            assert result["explanation"] is not None
            assert "deterministic" in data["disclaimer"].lower()
    finally:
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_candidate_intelligence_upstream_error():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter)

    try:
        with patch("app.ai.candidate_intelligence.service.candidate_intelligence_service.get_candidate_intelligence") as mock_ci:
            mock_ci.side_effect = RuntimeError("Matching engine failed")

            response = client.post(
                f"/recruiter/jobs/{job.id}/candidate-intelligence",
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 502
            assert "temporarily unavailable" in response.json()["detail"]
    finally:
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_candidate_intelligence_no_database_mutation():
    """Verify that candidate intelligence evaluation does not alter database state."""
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter)

    try:
        with patch("app.ai.candidate_intelligence.service.candidate_intelligence_service.get_candidate_intelligence") as mock_ci:
            mock_ci.return_value = make_mock_intelligence_response(job.id, job.title)

            response = client.post(
                f"/recruiter/jobs/{job.id}/candidate-intelligence",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 200

            db.refresh(job)
            assert job.title == "Senior Python Backend Engineer"
            assert job.is_active is True
    finally:
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()
