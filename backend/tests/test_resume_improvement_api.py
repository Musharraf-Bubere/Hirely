from uuid import uuid4

from fastapi.testclient import TestClient

from app.ai.ats_analyzer.schemas import ATSScoreBreakdown
from app.ai.resume_improvement.schemas import (
    ActionPriority,
    ImprovementAction,
    ResumeImprovementResponse,
    ResumeImprovementResult,
    SectionImprovement,
    SectionStatus,
)
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

def create_test_candidate():
    """
    Create a temporary candidate user and profile.
    Returns: db, user, candidate, access_token.
    """
    db = SessionLocal()
    email = f"improve-cand-{uuid4()}@example.com"

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
        first_name="Test",
        last_name="Candidate",
        headline="Python Backend Engineer",
        bio="Test candidate for resume improvement API.",
        location="Bengaluru",
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )
    return db, user, candidate, token


def create_test_recruiter_and_job(db, *, is_active: bool = True):
    """
    Create a temporary recruiter and job in the database.
    """
    email = f"improve-rec-{uuid4()}@example.com"

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
        first_name="Hiring",
        last_name="Manager",
        job_title="Talent Lead",
        location="Bengaluru",
    )
    db.add(recruiter)
    db.commit()
    db.refresh(recruiter)

    job = Job(
        recruiter_id=recruiter.id,
        title="Python Backend Developer",
        description="Build high-performance microservices using Python and FastAPI.",
        location="Bengaluru",
        employment_type="Full-time",
        experience_level="Mid-level",
        salary_min=600000,
        salary_max=1200000,
        is_active=is_active,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    return user, recruiter, job


def cleanup_test_data(
    db,
    candidate=None,
    candidate_user=None,
    recruiter=None,
    recruiter_user=None,
    job=None,
):
    """
    Remove temporary database records in foreign-key-safe order.
    """
    if job:
        db.delete(job)
    if candidate:
        db.delete(candidate)
    if recruiter:
        db.delete(recruiter)
    if recruiter_user:
        db.delete(recruiter_user)
    if candidate_user:
        db.delete(candidate_user)
    db.commit()
    db.close()


def make_sample_api_response(job_id) -> ResumeImprovementResponse:
    score_breakdown = ATSScoreBreakdown(
        required_skill_score=0.85,
        preferred_skill_score=0.60,
        semantic_relevance_score=0.80,
        resume_completeness_score=0.90,
    )
    result = ResumeImprovementResult(
        overall_assessment="Strong Python alignment with minor gaps in distributed caching.",
        ats_score=81,
        score_breakdown=score_breakdown,
        missing_required_skills=["PostgreSQL"],
        missing_preferred_skills=["Redis"],
        prioritized_actions=[
            ImprovementAction(
                priority=ActionPriority.HIGH,
                category="Skills",
                title="Highlight PostgreSQL Production Experience",
                recommendation="If you used PostgreSQL in your projects, highlight indexing strategies.",
                rationale="PostgreSQL is required for this role.",
                requires_candidate_verification=True,
            )
        ],
        required_skill_recommendations=["Add PostgreSQL implementation details."],
        preferred_skill_recommendations=["Mention Redis caching if applicable."],
        section_improvements=[
            SectionImprovement(
                section_name="Work Experience",
                current_status=SectionStatus.NEEDS_IMPROVEMENT,
                suggestions=["Quantify API response time improvements."],
            )
        ],
        summary_improvements=["Mention backend scaling directly."],
        experience_improvements=["Add database optimization details."],
        project_improvements=["Detail architecture in project section."],
        skills_improvements=["Organize skills into Core and Tools."],
    )
    return ResumeImprovementResponse(
        job_id=job_id,
        resume_improvement=result,
    )


# =====================================================================
# API Tests
# =====================================================================

def test_resume_improvement_requires_authentication():
    response = client.post(
        "/candidate/resume-improvement",
        json={
            "job_id": str(uuid4()),
        },
    )
    assert response.status_code in {401, 403}


def test_resume_improvement_rejects_recruiter_role():
    db = SessionLocal()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    recruiter_token = create_access_token(
        user_id=str(recruiter_user.id),
        role=recruiter_user.role.value,
    )

    try:
        response = client.post(
            "/candidate/resume-improvement",
            headers={
                "Authorization": f"Bearer {recruiter_token}",
            },
            json={
                "job_id": str(job.id),
            },
        )
        assert response.status_code == 403
    finally:
        cleanup_test_data(
            db=db,
            recruiter=recruiter,
            recruiter_user=recruiter_user,
            job=job,
        )


def test_resume_improvement_rejects_missing_job():
    db, candidate_user, candidate, token = create_test_candidate()

    try:
        random_job_id = str(uuid4())
        response = client.post(
            "/candidate/resume-improvement",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": random_job_id,
            },
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"
    finally:
        cleanup_test_data(
            db=db,
            candidate=candidate,
            candidate_user=candidate_user,
        )


def test_resume_improvement_rejects_inactive_job():
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(
        db,
        is_active=False,
    )

    try:
        response = client.post(
            "/candidate/resume-improvement",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"
    finally:
        cleanup_test_data(
            db=db,
            candidate=candidate,
            candidate_user=candidate_user,
            recruiter=recruiter,
            recruiter_user=recruiter_user,
            job=job,
        )


def test_resume_improvement_returns_bad_request_without_active_resume(
    monkeypatch,
):
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    from app.api import candidate as candidate_api

    def mock_generate_improvement(db, candidate, job):
        raise ValueError("Candidate does not have an active resume.")

    monkeypatch.setattr(
        candidate_api.resume_improvement_service,
        "generate_improvement",
        mock_generate_improvement,
    )

    try:
        response = client.post(
            "/candidate/resume-improvement",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )
        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Candidate does not have an active resume."
        )
    finally:
        cleanup_test_data(
            db=db,
            candidate=candidate,
            candidate_user=candidate_user,
            recruiter=recruiter,
            recruiter_user=recruiter_user,
            job=job,
        )


def test_resume_improvement_returns_bad_request_with_incomplete_parsing(
    monkeypatch,
):
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    from app.api import candidate as candidate_api

    def mock_generate_improvement(db, candidate, job):
        raise ValueError(
            "Candidate's active resume has not been parsed successfully."
        )

    monkeypatch.setattr(
        candidate_api.resume_improvement_service,
        "generate_improvement",
        mock_generate_improvement,
    )

    try:
        response = client.post(
            "/candidate/resume-improvement",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )
        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Candidate's active resume has not been parsed successfully."
        )
    finally:
        cleanup_test_data(
            db=db,
            candidate=candidate,
            candidate_user=candidate_user,
            recruiter=recruiter,
            recruiter_user=recruiter_user,
            job=job,
        )


def test_resume_improvement_returns_bad_request_with_empty_parsed_data(
    monkeypatch,
):
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    from app.api import candidate as candidate_api

    def mock_generate_improvement(db, candidate, job):
        raise ValueError(
            "Candidate's active resume does not contain parsed data."
        )

    monkeypatch.setattr(
        candidate_api.resume_improvement_service,
        "generate_improvement",
        mock_generate_improvement,
    )

    try:
        response = client.post(
            "/candidate/resume-improvement",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )
        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Candidate's active resume does not contain parsed data."
        )
    finally:
        cleanup_test_data(
            db=db,
            candidate=candidate,
            candidate_user=candidate_user,
            recruiter=recruiter,
            recruiter_user=recruiter_user,
            job=job,
        )


def test_resume_improvement_returns_service_error_as_502(
    monkeypatch,
):
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    from app.api import candidate as candidate_api

    def mock_generate_improvement(db, candidate, job):
        raise RuntimeError("Gemini AI upstream timeout")

    monkeypatch.setattr(
        candidate_api.resume_improvement_service,
        "generate_improvement",
        mock_generate_improvement,
    )

    try:
        response = client.post(
            "/candidate/resume-improvement",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )
        assert response.status_code == 502
        assert response.json()["detail"] == (
            "Resume Improvement service is temporarily unavailable."
        )
    finally:
        cleanup_test_data(
            db=db,
            candidate=candidate,
            candidate_user=candidate_user,
            recruiter=recruiter,
            recruiter_user=recruiter_user,
            job=job,
        )


def test_resume_improvement_returns_valid_response(
    monkeypatch,
):
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    from app.api import candidate as candidate_api

    expected_response = make_sample_api_response(job.id)

    def mock_generate_improvement(db, candidate, job):
        return expected_response

    monkeypatch.setattr(
        candidate_api.resume_improvement_service,
        "generate_improvement",
        mock_generate_improvement,
    )

    try:
        response = client.post(
            "/candidate/resume-improvement",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )
        assert response.status_code == 200
        assert response.json() == expected_response.model_dump(mode="json")
    finally:
        cleanup_test_data(
            db=db,
            candidate=candidate,
            candidate_user=candidate_user,
            recruiter=recruiter,
            recruiter_user=recruiter_user,
            job=job,
        )


def test_resume_improvement_uses_authenticated_candidate(
    monkeypatch,
):
    """
    Ensure the candidate object passed to resume_improvement_service
    strictly belongs to the authenticated user from the token.
    """
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    from app.api import candidate as candidate_api

    invoked_candidate_id = []

    def mock_generate_improvement(db, candidate, job):
        invoked_candidate_id.append(candidate.id)
        return make_sample_api_response(job.id)

    monkeypatch.setattr(
        candidate_api.resume_improvement_service,
        "generate_improvement",
        mock_generate_improvement,
    )

    try:
        response = client.post(
            "/candidate/resume-improvement",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )
        assert response.status_code == 200
        assert len(invoked_candidate_id) == 1
        assert invoked_candidate_id[0] == candidate.id
    finally:
        cleanup_test_data(
            db=db,
            candidate=candidate,
            candidate_user=candidate_user,
            recruiter=recruiter,
            recruiter_user=recruiter_user,
            job=job,
        )
