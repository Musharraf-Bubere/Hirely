from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient

from app.ai.job_description_analyzer.schemas import (
    IssueCategory,
    IssuePriority,
    JobDescriptionAIResult,
    JobDescriptionIssue,
    JobSkillsAnalysis,
)
from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.models.recruiter import Recruiter
from app.models.skill import Skill
from app.models.user import User, UserRole


client = TestClient(app)


# =====================================================================
# Fixtures and Helpers
# =====================================================================

def create_test_recruiter(db, *, suffix: str = ""):
    email = f"jd-rec-{suffix}-{uuid4()}@example.com"
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
        first_name="Recruiter",
        last_name=f"Lead{suffix}",
        job_title="Hiring Manager",
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
    email = f"jd-cand-{uuid4()}@example.com"
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
        last_name="User",
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )
    return user, candidate, token


def create_test_job(db, recruiter, *, description="Build scalable Python backend services."):
    job = Job(
        recruiter_id=recruiter.id,
        title="Python Backend Engineer",
        description=description,
        location="Bengaluru",
        employment_type="Full-time",
        experience_level="Mid-level",
        salary_min=800000,
        salary_max=1400000,
        is_active=True,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def make_mock_ai_result() -> JobDescriptionAIResult:
    return JobDescriptionAIResult(
        quality_score=84,
        overall_assessment="Clear technical focus with well-defined core responsibilities.",
        strengths=["Clear stack defined.", "Realistic experience requirements."],
        issues=[
            JobDescriptionIssue(
                priority=IssuePriority.HIGH,
                category=IssueCategory.COMPLETENESS,
                title="Missing team hierarchy details",
                explanation="Does not specify reporting line.",
                suggested_action="Mention the engineering director or lead.",
            )
        ],
        missing_information=["Remote vs hybrid policy."],
        skills_analysis=JobSkillsAnalysis(
            required_skills_evaluation="Python is clearly stated as mandatory.",
            preferred_skills_evaluation="Docker is optional.",
            unmentioned_skills_in_description=[],
            suggested_skills_to_add=["Kubernetes"],
        ),
        improvement_recommendations=["Add team culture details."],
        improved_description="Revised draft with [Placeholders].",
    )


# =====================================================================
# API Tests
# =====================================================================

def test_job_description_analyzer_unauthenticated():
    response = client.post(f"/recruiter/jobs/{uuid4()}/description-analysis")
    assert response.status_code in (401, 403)


def test_job_description_analyzer_candidate_forbidden():
    db = SessionLocal()
    user, candidate, token = create_test_candidate(db)
    try:
        response = client.post(
            f"/recruiter/jobs/{uuid4()}/description-analysis",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
        assert "Insufficient permissions" in response.json()["detail"]
    finally:
        db.delete(candidate)
        db.delete(user)
        db.commit()
        db.close()


def test_job_description_analyzer_recruiter_profile_missing():
    db = SessionLocal()
    # Create recruiter user without profile
    user = User(
        email=f"noprofile-{uuid4()}@example.com",
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
            f"/recruiter/jobs/{uuid4()}/description-analysis",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        assert "Recruiter profile not found" in response.json()["detail"]
    finally:
        db.delete(user)
        db.commit()
        db.close()


def test_job_description_analyzer_missing_job():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    missing_job_id = uuid4()
    try:
        response = client.post(
            f"/recruiter/jobs/{missing_job_id}/description-analysis",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
        assert "Job not found" in response.json()["detail"]
    finally:
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_job_description_analyzer_ownership_forbidden():
    """Recruiter A cannot analyze a job belonging to Recruiter B."""
    db = SessionLocal()
    user_a, recruiter_a, token_a = create_test_recruiter(db, suffix="a")
    user_b, recruiter_b, _ = create_test_recruiter(db, suffix="b")
    job_b = create_test_job(db, recruiter_b)

    try:
        response = client.post(
            f"/recruiter/jobs/{job_b.id}/description-analysis",
            headers={"Authorization": f"Bearer {token_a}"},
        )
        assert response.status_code == 403
        assert "permission to analyze" in response.json()["detail"].lower()
    finally:
        db.delete(job_b)
        db.delete(recruiter_a)
        db.delete(user_a)
        db.delete(recruiter_b)
        db.delete(user_b)
        db.commit()
        db.close()


def test_job_description_analyzer_empty_description():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter, description="   ")

    try:
        response = client.post(
            f"/recruiter/jobs/{job.id}/description-analysis",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 400
        assert "description cannot be empty" in response.json()["detail"].lower()
    finally:
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_job_description_analyzer_success():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter, description="Develop real-time distributed microservices with Python, FastAPI, and Kafka.")

    skill = Skill(name=f"Python-{uuid4()}")
    db.add(skill)
    db.commit()
    db.refresh(skill)

    js = JobSkill(job_id=job.id, skill_id=skill.id, is_required=True)
    db.add(js)
    db.commit()

    try:
        with patch("app.ai.job_description_analyzer.service.gemini_service.generate_structured") as mock_gemini:
            mock_gemini.return_value = make_mock_ai_result()

            response = client.post(
                f"/recruiter/jobs/{job.id}/description-analysis",
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == str(job.id)
            assert "analysis" in data
            analysis = data["analysis"]
            assert analysis["quality_score"] == 84
            assert len(analysis["strengths"]) == 2
            assert len(analysis["issues"]) == 1
            assert analysis["issues"][0]["priority"] == "high"
            assert "skills_analysis" in analysis
            assert "heuristic evaluation" in analysis["disclaimer"]
            assert analysis["improved_description"] is not None
    finally:
        db.delete(js)
        db.delete(skill)
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()


def test_job_description_analyzer_upstream_ai_failure():
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    job = create_test_job(db, recruiter)

    try:
        with patch("app.ai.job_description_analyzer.service.gemini_service.generate_structured") as mock_gemini:
            mock_gemini.side_effect = Exception("Gemini service unavailable")

            response = client.post(
                f"/recruiter/jobs/{job.id}/description-analysis",
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


def test_job_description_analyzer_no_database_mutation():
    """Verify that calling the analyzer does not mutate the job or database records."""
    db = SessionLocal()
    user, recruiter, token = create_test_recruiter(db)
    original_desc = "Original immutable job description."
    job = create_test_job(db, recruiter, description=original_desc)

    try:
        with patch("app.ai.job_description_analyzer.service.gemini_service.generate_structured") as mock_gemini:
            mock_gemini.return_value = make_mock_ai_result()

            response = client.post(
                f"/recruiter/jobs/{job.id}/description-analysis",
                headers={"Authorization": f"Bearer {token}"},
            )

            assert response.status_code == 200

            # Re-fetch from DB and verify unchanged
            db.refresh(job)
            assert job.description == original_desc
            assert job.title == "Python Backend Engineer"
            assert job.is_active is True
    finally:
        db.delete(job)
        db.delete(recruiter)
        db.delete(user)
        db.commit()
        db.close()
