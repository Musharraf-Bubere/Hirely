from uuid import uuid4

import pytest

from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.resume import Resume
from app.models.user import User, UserRole
from app.core.security import hash_password, create_access_token


client = TestClient(app)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_user(db, role: UserRole):
    user = User(
        email=f"{role.value}-{uuid4()}@example.com",
        password_hash=hash_password("TestPassword123!"),
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_candidate(db, user):
    candidate = Candidate(
        user_id=user.id,
        first_name="Test",
        last_name="Candidate",
        headline="Python Developer",
        bio="Recruiter matching test candidate.",
        location="India",
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


def create_recruiter(db, user):
    recruiter = Recruiter(
        user_id=user.id,
        first_name="Test",
        last_name="Recruiter",
        job_title="Technical Recruiter",
        location="India",
    )

    db.add(recruiter)
    db.commit()
    db.refresh(recruiter)

    return recruiter


def create_job(db, recruiter, is_active=True):
    job = Job(
        recruiter_id=recruiter.id,
        title="Python Backend Developer",
        description=(
            "Build scalable backend services using Python and FastAPI."
        ),
        location="Remote",
        employment_type="FULL_TIME",
        experience_level="MID",
        salary_min=800000,
        salary_max=1400000,
        is_active=is_active,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def create_completed_resume(db, candidate):
    resume = Resume(
        candidate_id=candidate.id,
        original_filename="resume.pdf",
        file_path="test.pdf",
        parsing_status="COMPLETED",
        is_active=True,
        parsed_data={
            "name": "Test Candidate",
            "email": "candidate@example.com",
            "phone": "9999999999",
            "summary": "Python backend developer",
            "skills": [
                "Python",
                "FastAPI",
                "SQL",
            ],
            "experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
        },
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def token_for(user):
    return create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )


# ---------------------------------------------------------
# 1. Recruiter can access own job
# ---------------------------------------------------------

def test_recruiter_can_match_candidates_for_own_job():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None
    resume = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        resume = create_completed_resume(
            db,
            candidate,
        )

        job = create_job(
            db,
            recruiter,
        )

        token = token_for(recruiter_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Recruiter matching status:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 200

        results = response.json()

        assert isinstance(results, list)

        if results:
            assert results[0]["rank"] == 1
            assert "candidate_id" in results[0]
            assert "overall_score" in results[0]
            assert "required_skill_score" in results[0]
            assert "semantic_similarity" in results[0]

    finally:
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 2. Candidate cannot access recruiter endpoint
# ---------------------------------------------------------

def test_candidate_cannot_match_candidates():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        job = create_job(
            db,
            recruiter,
        )

        token = token_for(candidate_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Candidate → recruiter matching:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 403

    finally:
        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 3. Unauthenticated request
# ---------------------------------------------------------

def test_recruiter_matching_requires_authentication():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        response = client.post(
            f"/jobs/{job.id}/candidates/match",
        )

        print("Unauthenticated recruiter matching:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 401

    finally:
        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 4. Nonexistent job
# ---------------------------------------------------------

def test_recruiter_matching_rejects_nonexistent_job():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        token = token_for(recruiter_user)

        fake_job_id = uuid4()

        response = client.post(
            f"/jobs/{fake_job_id}/candidates/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Nonexistent job:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 404

    finally:
        if recruiter:
            db.delete(recruiter)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 5. Inactive job
# ---------------------------------------------------------

def test_recruiter_matching_rejects_inactive_job():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        job = create_job(
            db,
            recruiter,
            is_active=False,
        )

        token = token_for(recruiter_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Inactive job:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 404

    finally:
        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 6. Recruiter cannot access another recruiter's job
# ---------------------------------------------------------

def test_recruiter_cannot_match_candidates_for_another_recruiters_job():
    db = SessionLocal()

    recruiter_a_user = None
    recruiter_a = None

    recruiter_b_user = None
    recruiter_b = None

    job = None

    try:
        recruiter_a_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter_a = create_recruiter(
            db,
            recruiter_a_user,
        )

        recruiter_b_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter_b = create_recruiter(
            db,
            recruiter_b_user,
        )

        job = create_job(
            db,
            recruiter_a,
        )

        token = token_for(recruiter_b_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Cross-recruiter access:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 403

    finally:
        if job:
            db.delete(job)

        if recruiter_a:
            db.delete(recruiter_a)

        if recruiter_b:
            db.delete(recruiter_b)

        if recruiter_a_user:
            db.delete(recruiter_a_user)

        if recruiter_b_user:
            db.delete(recruiter_b_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 7. Candidate without active resume is skipped
# ---------------------------------------------------------

def test_recruiter_matching_skips_candidates_without_active_resume():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        token = token_for(recruiter_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("No eligible resume:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 200

        results = response.json()

        candidate_ids = {
            result["candidate_id"]
            for result in results
        }

        assert str(candidate.id) not in candidate_ids

    finally:
        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 8. Candidate with pending resume is skipped
# ---------------------------------------------------------

def test_recruiter_matching_skips_pending_resume():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    job = None
    resume = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        resume = Resume(
            candidate_id=candidate.id,
            original_filename="resume.pdf",
            file_path="test.pdf",
            parsing_status="PENDING",
            is_active=True,
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        job = create_job(
            db,
            recruiter,
        )

        token = token_for(recruiter_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Pending resume:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 200

        results = response.json()

        candidate_ids = {
            result["candidate_id"]
            for result in results
        }

        assert str(candidate.id) not in candidate_ids

    finally:
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()

# ---------------------------------------------------------
# 9. Stronger candidate ranks above weaker candidate
# ---------------------------------------------------------

def test_recruiter_matching_ranks_stronger_candidate_first(
    monkeypatch,
):
    db = SessionLocal()

    recruiter_user = None
    recruiter = None

    strong_candidate_user = None
    strong_candidate = None
    strong_resume = None

    weak_candidate_user = None
    weak_candidate = None
    weak_resume = None

    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        # -------------------------------------------------
        # Strong candidate
        # -------------------------------------------------

        strong_candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        strong_candidate = create_candidate(
            db,
            strong_candidate_user,
        )

        strong_resume = Resume(
            candidate_id=strong_candidate.id,
            original_filename="strong_resume.pdf",
            file_path="strong_test.pdf",
            parsing_status="COMPLETED",
            is_active=True,
            parsed_data={
                "name": "Strong Candidate",
                "email": "strong@example.com",
                "phone": "9999999999",
                "summary": (
                    "Experienced Python backend developer "
                    "with FastAPI and SQL experience."
                ),
                "skills": [
                    "Python",
                    "FastAPI",
                    "SQL",
                ],
                "experience": [],
                "projects": [],
                "education": [],
                "certifications": [],
            },
        )

        db.add(strong_resume)

        # -------------------------------------------------
        # Weak candidate
        # -------------------------------------------------

        weak_candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        weak_candidate = create_candidate(
            db,
            weak_candidate_user,
        )

        weak_resume = Resume(
            candidate_id=weak_candidate.id,
            original_filename="weak_resume.pdf",
            file_path="weak_test.pdf",
            parsing_status="COMPLETED",
            is_active=True,
            parsed_data={
                "name": "Weak Candidate",
                "email": "weak@example.com",
                "phone": "9999999999",
                "summary": (
                    "Graphic designer with experience "
                    "in visual design."
                ),
                "skills": [
                    "Photoshop",
                    "Illustrator",
                    "Figma",
                ],
                "experience": [],
                "projects": [],
                "education": [],
                "certifications": [],
            },
        )

        db.add(weak_resume)

        # -------------------------------------------------
        # Job
        # -------------------------------------------------

        job = create_job(
            db,
            recruiter,
        )

        db.commit()

        # -------------------------------------------------
        # Mock embeddings
        # -------------------------------------------------

        def fake_embed_text(self, text):
            if "Python backend developer" in text:
                return [1.0, 0.0, 0.0]

            if "Graphic designer" in text:
                return [0.0, 1.0, 0.0]

            return [1.0, 0.0, 0.0]

        monkeypatch.setattr(
            "app.ai.embeddings.service.EmbeddingService.embed_text",
            fake_embed_text,
        )

        token = token_for(recruiter_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Ranking status:", response.status_code)
        print("Ranking response:", response.json())

        assert response.status_code == 200

        results = response.json()

        # Find our two candidates in the results.
        result_by_candidate = {
            result["candidate_id"]: result
            for result in results
        }

        assert str(strong_candidate.id) in result_by_candidate
        assert str(weak_candidate.id) in result_by_candidate

        strong_result = result_by_candidate[
            str(strong_candidate.id)
        ]

        weak_result = result_by_candidate[
            str(weak_candidate.id)
        ]

        # Strong candidate must score higher.
        assert (
            strong_result["overall_score"]
            > weak_result["overall_score"]
        )

        # Therefore strong candidate must rank first.
        assert strong_result["rank"] < weak_result["rank"]

    finally:
        if strong_resume:
            db.delete(strong_resume)

        if weak_resume:
            db.delete(weak_resume)

        if strong_candidate:
            db.delete(strong_candidate)

        if weak_candidate:
            db.delete(weak_candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if strong_candidate_user:
            db.delete(strong_candidate_user)

        if weak_candidate_user:
            db.delete(weak_candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()

# ---------------------------------------------------------
# 10. Real Gemini recruiter matching integration test
# ---------------------------------------------------------

@pytest.mark.integration
def test_recruiter_matching_with_real_gemini():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    resume = None
    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        resume = create_completed_resume(
            db,
            candidate,
        )

        job = create_job(
            db,
            recruiter,
        )

        token = token_for(recruiter_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Real Gemini matching status:", response.status_code)
        print("Real Gemini matching response:", response.json())

        assert response.status_code == 200

        results = response.json()

        assert isinstance(results, list)

        # Our candidate should be present because they have
        # an active, completed resume.
        candidate_ids = {
            result["candidate_id"]
            for result in results
        }

        assert str(candidate.id) in candidate_ids

        result = next(
            item
            for item in results
            if item["candidate_id"] == str(candidate.id)
        )

        # Verify the real matching pipeline returned
        # meaningful matching signals.
        assert "rank" in result
        assert "overall_score" in result
        assert "required_skill_score" in result
        assert "preferred_skill_score" in result
        assert "semantic_similarity" in result

        assert 0.0 <= result["overall_score"] <= 1.0
        assert 0.0 <= result["required_skill_score"] <= 1.0
        assert 0.0 <= result["semantic_similarity"] <= 1.0

    finally:
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()

# ---------------------------------------------------------
# 11. Recruiter matching explanation endpoint
# ---------------------------------------------------------

def test_recruiter_matching_explanation_returns_top_n_explanations(
    monkeypatch,
):
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    candidate = None
    resume = None
    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        candidate = create_candidate(
            db,
            candidate_user,
        )

        resume = create_completed_resume(
            db,
            candidate,
        )

        job = create_job(
            db,
            recruiter,
        )

        db.commit()

        # -------------------------------------------------
        # Mock embeddings
        # -------------------------------------------------

        def fake_embed_text(self, text):
            return [1.0, 0.0, 0.0]

        monkeypatch.setattr(
            "app.ai.embeddings.service.EmbeddingService.embed_text",
            fake_embed_text,
        )

        # -------------------------------------------------
        # Mock Gemini explanation
        # -------------------------------------------------

        from app.ai.matching.explanation import (
            MatchExplanation,
            MatchExplanationEvidence,
        )

        def fake_explain(data):
            return MatchExplanation(
                summary="Candidate matches the job based on the provided evidence.",
                strengths=["Python", "FastAPI"],
                gaps=["No preferred skill evidence"],
                evidence=MatchExplanationEvidence(
                    required_skill_score=data.required_skill_score,
                    preferred_skill_score=data.preferred_skill_score,
                    semantic_similarity=data.semantic_similarity,
                ),
                caveats=[
                    "The explanation is based only on the available matching evidence."
                ],
            )

        monkeypatch.setattr(
            "app.ai.services.match_explanation_service.match_explanation_service.explain",
            fake_explain,
        )

        token = token_for(recruiter_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match/explain",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Explanation endpoint status:",
            response.status_code,
        )
        print(
            "Explanation response:",
            response.json(),
        )

        assert response.status_code == 200

        results = response.json()

        assert isinstance(results, list)
        assert results

        result = next(
            item
            for item in results
            if item["match"]["candidate_id"]
            == str(candidate.id)
        )

        # -------------------------------------------------
        # Verify FinalMatchResult structure
        # -------------------------------------------------

        assert "match" in result
        assert "explanation" in result

        assert result["match"]["candidate_id"] == str(
            candidate.id
        )

        assert result["explanation"] is not None

        # -------------------------------------------------
        # Verify explanation fields
        # -------------------------------------------------

        explanation = result["explanation"]

        assert "summary" in explanation
        assert "strengths" in explanation
        assert "gaps" in explanation
        assert "evidence" in explanation
        assert "caveats" in explanation

        assert explanation["summary"]
        assert isinstance(explanation["strengths"], list)
        assert isinstance(explanation["gaps"], list)
        assert isinstance(explanation["caveats"], list)

        # -------------------------------------------------
        # Verify evidence comes from matching result
        # -------------------------------------------------

        assert (
            explanation["evidence"]["required_skill_score"]
            == result["match"]["required_skill_score"]
        )

        assert (
            explanation["evidence"]["semantic_similarity"]
            == result["match"]["semantic_similarity"]
        )

    finally:
        if resume:
            db.delete(resume)

        if candidate:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 12. Explanation limit only explains Top N candidates
# ---------------------------------------------------------

def test_recruiter_matching_explanation_limit(
    monkeypatch,
):
    db = SessionLocal()

    recruiter_user = None
    recruiter = None

    candidate_users = []
    candidates = []
    resumes = []

    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        # -------------------------------------------------
        # Create multiple eligible candidates
        # -------------------------------------------------

        for _ in range(3):
            candidate_user = create_user(
                db,
                UserRole.CANDIDATE,
            )

            candidate = create_candidate(
                db,
                candidate_user,
            )

            resume = create_completed_resume(
                db,
                candidate,
            )

            candidate_users.append(candidate_user)
            candidates.append(candidate)
            resumes.append(resume)

        job = create_job(
            db,
            recruiter,
        )

        db.commit()

        # -------------------------------------------------
        # Mock embeddings
        # -------------------------------------------------

        def fake_embed_text(self, text):
            return [1.0, 0.0, 0.0]

        monkeypatch.setattr(
            "app.ai.embeddings.service.EmbeddingService.embed_text",
            fake_embed_text,
        )

        # -------------------------------------------------
        # Track explanation calls
        # -------------------------------------------------

        from app.ai.matching.explanation import (
            MatchExplanation,
            MatchExplanationEvidence,
        )

        explained_candidate_ids = []

        def fake_explain(data):
            explained_candidate_ids.append(
                str(data.candidate_id)
            )

            return MatchExplanation(
                summary="Mock explanation",
                strengths=[],
                gaps=[],
                evidence=MatchExplanationEvidence(
                    required_skill_score=data.required_skill_score,
                    preferred_skill_score=data.preferred_skill_score,
                    semantic_similarity=data.semantic_similarity,
                ),
                caveats=[],
            )

        monkeypatch.setattr(
            "app.ai.services.match_explanation_service.match_explanation_service.explain",
            fake_explain,
        )

        token = token_for(recruiter_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match/explain",
            params={
                "explanation_limit": 1,
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Explanation limit status:",
            response.status_code,
        )
        print(
            "Explanation limit response:",
            response.json(),
        )

        assert response.status_code == 200

        results = response.json()

        assert isinstance(results, list)

        # -------------------------------------------------
        # Exactly one candidate should receive an explanation
        # -------------------------------------------------

        explained_results = [
            result
            for result in results
            if result["explanation"] is not None
        ]

        unexplained_results = [
            result
            for result in results
            if result["explanation"] is None
        ]

        assert len(explained_results) == 1

        assert len(explained_results) + len(
            unexplained_results
        ) == len(results)

        # -------------------------------------------------
        # Only one Gemini explanation call should happen
        # -------------------------------------------------

        assert len(explained_candidate_ids) == 1

        explained_candidate_id = (
            explained_results[0]["match"]["candidate_id"]
        )

        assert (
            explained_candidate_id
            == explained_candidate_ids[0]
        )

        # -------------------------------------------------
        # The explained candidate must be Rank 1
        # -------------------------------------------------

        assert (
            explained_results[0]["match"]["rank"]
            == 1
        )

    finally:
        for resume in resumes:
            db.delete(resume)

        for candidate in candidates:
            db.delete(candidate)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        for candidate_user in candidate_users:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 13. Candidate cannot access explanation endpoint
# ---------------------------------------------------------

def test_candidate_cannot_access_matching_explanation_endpoint():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    candidate_user = None
    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        candidate_user = create_user(
            db,
            UserRole.CANDIDATE,
        )

        job = create_job(
            db,
            recruiter,
        )

        token = token_for(candidate_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match/explain",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Candidate explanation access:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 403

    finally:
        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if candidate_user:
            db.delete(candidate_user)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 14. Unauthenticated explanation request
# ---------------------------------------------------------

def test_matching_explanation_requires_authentication():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        response = client.post(
            f"/jobs/{job.id}/candidates/match/explain",
        )

        print(
            "Unauthenticated explanation:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 401

    finally:
        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 15. Cross-recruiter explanation access is forbidden
# ---------------------------------------------------------

def test_recruiter_cannot_explain_candidates_for_another_recruiters_job():
    db = SessionLocal()

    recruiter_a_user = None
    recruiter_a = None

    recruiter_b_user = None
    recruiter_b = None

    job = None

    try:
        recruiter_a_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter_a = create_recruiter(
            db,
            recruiter_a_user,
        )

        recruiter_b_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter_b = create_recruiter(
            db,
            recruiter_b_user,
        )

        job = create_job(
            db,
            recruiter_a,
        )

        token = token_for(recruiter_b_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match/explain",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Cross-recruiter explanation:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 403

    finally:
        if job:
            db.delete(job)

        if recruiter_a:
            db.delete(recruiter_a)

        if recruiter_b:
            db.delete(recruiter_b)

        if recruiter_a_user:
            db.delete(recruiter_a_user)

        if recruiter_b_user:
            db.delete(recruiter_b_user)

        db.commit()
        db.close()


# ---------------------------------------------------------
# 16. Invalid explanation limit
# ---------------------------------------------------------

def test_matching_explanation_rejects_invalid_explanation_limit():
    db = SessionLocal()

    recruiter_user = None
    recruiter = None
    job = None

    try:
        recruiter_user = create_user(
            db,
            UserRole.RECRUITER,
        )

        recruiter = create_recruiter(
            db,
            recruiter_user,
        )

        job = create_job(
            db,
            recruiter,
        )

        token = token_for(recruiter_user)

        response = client.post(
            f"/jobs/{job.id}/candidates/match/explain",
            params={
                "explanation_limit": 0,
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print(
            "Invalid explanation limit:",
            response.status_code,
        )
        print(
            "Response:",
            response.json(),
        )

        assert response.status_code == 422

    finally:
        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if recruiter_user:
            db.delete(recruiter_user)

        db.commit()
        db.close()