from uuid import uuid4

from fastapi.testclient import TestClient

from app.ai.ats_analyzer.schemas import (
    ATSAnalysisResponse,
    ATSAnalysisResult,
    ATSScoreBreakdown,
)
from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.user import User, UserRole


client = TestClient(app)


def create_test_candidate():
    """
    Create a temporary candidate and return:
    database session, user, candidate, and JWT token.
    """
    db = SessionLocal()

    email = f"ats-validation-{uuid4()}@example.com"

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
        headline="Python Developer",
        bio="ATS Analyzer API validation test candidate.",
        location="India",
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    token = create_access_token(
        user_id=str(user.id),
        role=user.role.value,
    )

    return db, user, candidate, token


def create_test_recruiter_and_job(db):
    """
    Create a temporary recruiter and active job.
    """
    email = f"ats-recruiter-{uuid4()}@example.com"

    user = User(
        email=email,
        password_hash=hash_password("TestPassword123!"),
        role=UserRole.RECRUITER,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    recruiter = Recruiter(
        user_id=user.id,
        first_name="Test",
        last_name="Recruiter",
        job_title="Hiring Manager",
        location="India",
    )

    db.add(recruiter)
    db.commit()
    db.refresh(recruiter)

    job = Job(
        recruiter_id=recruiter.id,
        title="Python Backend Developer",
        description=(
            "Build backend APIs using Python and FastAPI."
        ),
        location="Mumbai",
        employment_type="Full-time",
        experience_level="Mid-level",
        salary_min=500000,
        salary_max=1000000,
        is_active=True,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return user, recruiter, job


def cleanup_test_data(
    db,
    candidate,
    candidate_user,
    recruiter,
    recruiter_user,
    job=None,
):
    """
    Remove temporary ATS test data in foreign-key-safe order.
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


def test_ats_analysis_requires_authentication():
    response = client.post(
        "/candidate/ats-analysis",
        json={
            "job_id": str(uuid4()),
        },
    )

    assert response.status_code in {401, 403}


def test_ats_analysis_rejects_invalid_job():
    db, candidate_user, candidate, token = create_test_candidate()

    try:
        response = client.post(
            "/candidate/ats-analysis",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(uuid4()),
            },
        )

        print("Invalid job:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"

    finally:
        cleanup_test_data(
            db=db,
            candidate=candidate,
            candidate_user=candidate_user,
            recruiter=None,
            recruiter_user=None,
        )


def test_ats_analysis_returns_bad_request_without_active_resume(
    monkeypatch,
):
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    from app.api import candidate as candidate_api

    def mock_generate_analysis(db, candidate, job):
        raise ValueError(
            "Candidate does not have an active resume."
        )

    monkeypatch.setattr(
        candidate_api.ats_analyzer_service,
        "generate_analysis",
        mock_generate_analysis,
    )

    try:
        response = client.post(
            "/candidate/ats-analysis",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )

        print("Missing resume:", response.status_code)
        print("Response:", response.json())

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


def test_ats_analysis_returns_service_error_as_502(
    monkeypatch,
):
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    from app.api import candidate as candidate_api

    def mock_generate_analysis(db, candidate, job):
        raise RuntimeError("AI service unavailable")

    monkeypatch.setattr(
        candidate_api.ats_analyzer_service,
        "generate_analysis",
        mock_generate_analysis,
    )

    try:
        response = client.post(
            "/candidate/ats-analysis",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )

        print("Service failure:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 502
        assert response.json()["detail"] == (
            "ATS Analysis service is temporarily unavailable."
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


def test_ats_analysis_returns_valid_response(
    monkeypatch,
):
    db, candidate_user, candidate, token = create_test_candidate()
    recruiter_user, recruiter, job = create_test_recruiter_and_job(db)

    from app.api import candidate as candidate_api

    expected_response = ATSAnalysisResponse(
        job_id=job.id,
        ats_analysis=ATSAnalysisResult(
            ats_score=82,
            score_breakdown=ATSScoreBreakdown(
                required_skill_score=0.9,
                preferred_skill_score=0.7,
                semantic_relevance_score=0.8,
                resume_completeness_score=0.9,
            ),
            required_skills_matched=[
                "Python",
                "FastAPI",
            ],
            required_skills_missing=[
                "PostgreSQL",
            ],
            preferred_skills_matched=[
                "Docker",
            ],
            preferred_skills_missing=[],
            strengths=[
                "Strong backend development experience.",
            ],
            improvement_areas=[
                "Add stronger evidence of PostgreSQL experience.",
            ],
            suggestions=[
                "Highlight relevant backend projects.",
            ],
            summary=(
                "The resume shows strong alignment with "
                "the selected backend role."
            ),
        ),
    )

    def mock_generate_analysis(db, candidate, job):
        return expected_response

    monkeypatch.setattr(
        candidate_api.ats_analyzer_service,
        "generate_analysis",
        mock_generate_analysis,
    )

    try:
        response = client.post(
            "/candidate/ats-analysis",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "job_id": str(job.id),
            },
        )

        print("Valid ATS analysis:", response.status_code)
        print("Response:", response.json())

        assert response.status_code == 200
        assert response.json() == expected_response.model_dump(
            mode="json"
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