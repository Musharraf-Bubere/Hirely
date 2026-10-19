from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

from app.ai.rag.schemas import (
    CandidateEvidenceResponse,
    EvidenceCitation,
)
from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)


def create_test_recruiter(db, *, suffix: str = ""):
    email = f"rag-rec-{suffix}-{uuid4()}@example.com"
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
        job_title="Talent Acquisition",
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
    email = f"rag-cand-{uuid4()}@example.com"
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
        first_name="Dev",
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
        title="Senior Cloud Architect",
        description="Design and manage multi-region cloud infrastructures.",
        location="Bengaluru",
        employment_type="Full-time",
        experience_level="Senior",
        is_active=is_active,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


# =====================================================================
# API Endpoint Tests
# =====================================================================

def test_rag_api_unauthenticated():
    response = client.post(f"/recruiter/jobs/{uuid4()}/candidates/{uuid4()}/ask-evidence")
    assert response.status_code in (401, 403)


def test_rag_api_candidate_forbidden():
    db = SessionLocal()
    user, candidate, token = create_test_candidate(db)
    try:
        response = client.post(
            f"/recruiter/jobs/{uuid4()}/candidates/{candidate.id}/ask-evidence",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "Cloud experience"},
        )
        assert response.status_code == 403
        assert "Insufficient permissions" in response.json()["detail"]
    finally:
        db.delete(candidate)
        db.delete(user)
        db.commit()
        db.close()


def test_rag_api_recruiter_profile_missing():
    db = SessionLocal()
    user = User(
        email=f"noprofile-rag-{uuid4()}@example.com",
        password_hash=hash_password("Pass123!"),
        role=UserRole.RECRUITER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user_id=str(user.id), role=user.role.value)

    try:
        response = client.post(
            f"/recruiter/jobs/{uuid4()}/candidates/{uuid4()}/ask-evidence",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "Cloud experience"},
        )
        assert response.status_code == 404
        assert "Recruiter profile not found" in response.json()["detail"]
    finally:
        db.delete(user)
        db.commit()
        db.close()


def test_rag_api_job_not_found():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    try:
        response = client.post(
            f"/recruiter/jobs/{uuid4()}/candidates/{uuid4()}/ask-evidence",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "Cloud experience"},
        )
        assert response.status_code == 404
        assert "Job not found" in response.json()["detail"]
    finally:
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_rag_api_ownership_forbidden():
    """Recruiter A cannot ask candidate evidence on a job owned by Recruiter B."""
    db = SessionLocal()
    user_a, recruiter_a, token_a = create_test_recruiter(db, suffix="a")
    user_b, recruiter_b, _ = create_test_recruiter(db, suffix="b")
    job_b = create_test_job(db, recruiter_b)

    try:
        response = client.post(
            f"/recruiter/jobs/{job_b.id}/candidates/{uuid4()}/ask-evidence",
            headers={"Authorization": f"Bearer {token_a}"},
            json={"query": "Cloud experience"},
        )
        assert response.status_code == 403
        assert "permission to query candidate evidence" in response.json()["detail"].lower()
    finally:
        db.delete(job_b)
        db.delete(recruiter_a)
        db.delete(user_a)
        db.delete(recruiter_b)
        db.delete(user_b)
        db.commit()
        db.close()


def test_rag_api_inactive_job():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter, is_active=False)

    try:
        response = client.post(
            f"/recruiter/jobs/{job.id}/candidates/{uuid4()}/ask-evidence",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "Cloud experience"},
        )
        assert response.status_code == 400
        assert "inactive" in response.json()["detail"].lower()
    finally:
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_rag_api_candidate_not_found():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter)

    try:
        response = client.post(
            f"/recruiter/jobs/{job.id}/candidates/{uuid4()}/ask-evidence",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "Cloud experience"},
        )
        assert response.status_code == 404
        assert "Candidate not found" in response.json()["detail"]
    finally:
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_rag_api_query_validation():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter)

    try:
        # Query too short (< 3 chars)
        response = client.post(
            f"/recruiter/jobs/{job.id}/candidates/{uuid4()}/ask-evidence",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": "ab"},
        )
        assert response.status_code == 422
    finally:
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_rag_api_happy_path_success():
    db = SessionLocal()
    user_rec, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter)
    user_cand, candidate, _ = create_test_candidate(db)

    try:
        mock_response = CandidateEvidenceResponse(
            candidate_id=candidate.id,
            job_id=job.id,
            query="Distributed Kafka architecture",
            has_evidence=True,
            confidence="high",
            answer="The candidate architected Kafka clusters processing 100k TPS.",
            citations=[
                EvidenceCitation(
                    source_id="exp_0",
                    section="experience",
                    organization="FinTech Corp",
                    role="Lead Architect",
                    timeframe="2021 - Present",
                    quote="Engineered core transaction engine processing 100k TPS with Apache Kafka.",
                )
            ],
            retrieved_chunk_count=2,
        )

        with patch("app.ai.rag.service.candidate_evidence_rag_service.ask_candidate_evidence") as mock_service:
            mock_service.return_value = mock_response

            response = client.post(
                f"/recruiter/jobs/{job.id}/candidates/{candidate.id}/ask-evidence",
                headers={"Authorization": f"Bearer {token}"},
                json={"query": "Distributed Kafka architecture", "top_k": 4},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["candidate_id"] == str(candidate.id)
            assert data["job_id"] == str(job.id)
            assert data["has_evidence"] is True
            assert data["confidence"] == "high"
            assert len(data["citations"]) == 1
            assert data["citations"][0]["organization"] == "FinTech Corp"
            assert "strictly from the candidate's active resume" in data["disclaimer"]
    finally:
        db.delete(candidate)
        db.delete(user_cand)
        db.delete(job)
        db.delete(recruiter)
        db.delete(user_rec)
        db.commit()
        db.close()


def test_rag_api_upstream_failure_returns_502():
    db = SessionLocal()
    user_rec, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter)
    user_cand, candidate, _ = create_test_candidate(db)

    try:
        with patch("app.ai.rag.service.candidate_evidence_rag_service.ask_candidate_evidence") as mock_service:
            mock_service.side_effect = RuntimeError("Embedding service connection timed out")

            response = client.post(
                f"/recruiter/jobs/{job.id}/candidates/{candidate.id}/ask-evidence",
                headers={"Authorization": f"Bearer {token}"},
                json={"query": "Distributed Kafka architecture"},
            )

            assert response.status_code == 502
            assert "temporarily unavailable" in response.json()["detail"]
    finally:
        db.delete(candidate)
        db.delete(user_cand)
        db.delete(job)
        db.delete(recruiter)
        db.delete(user_rec)
        db.commit()
        db.close()
