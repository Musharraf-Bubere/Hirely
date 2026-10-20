from uuid import uuid4
from fastapi.testclient import TestClient
import pytest

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.company import Company
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.resume import Resume
from app.models.user import User, UserRole

client = TestClient(app)


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_jobs_pagination_validation():
    # Negative skip -> 422
    resp = client.get("/jobs?skip=-1")
    assert resp.status_code == 422

    # Zero limit -> 422 (ge=1)
    resp = client.get("/jobs?limit=0")
    assert resp.status_code == 422

    # Limit exceeding 100 -> 422 (le=100)
    resp = client.get("/jobs?limit=101")
    assert resp.status_code == 422

    # Valid default -> 200
    resp = client.get("/jobs?skip=0&limit=20")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_jobs_pagination_slicing_and_stable_ordering(db_session):
    # Create recruiter and 5 active jobs
    user = User(
        email=f"recruiter-page-{uuid4()}@example.com",
        password_hash=hash_password("Password123!"),
        role=UserRole.RECRUITER,
    )
    db_session.add(user)
    db_session.commit()

    company = Company(name=f"Company-{uuid4()}", website="https://example.com")
    db_session.add(company)
    db_session.commit()

    recruiter = Recruiter(
        user_id=user.id,
        company_id=company.id,
        first_name="Recruiter",
        last_name="Page",
    )
    db_session.add(recruiter)
    db_session.commit()

    jobs = []
    for i in range(5):
        job = Job(
            recruiter_id=recruiter.id,
            title=f"Page Job {i}",
            description="Pagination test job description",
            location="Remote",
            employment_type="Full-time",
            experience_level="Mid",
            is_active=True,
        )
        db_session.add(job)
        jobs.append(job)
    db_session.commit()

    try:
        # Page 1: limit 2
        resp1 = client.get("/jobs?skip=0&limit=2")
        assert resp1.status_code == 200
        page1 = resp1.json()
        assert len(page1) == 2

        # Page 2: limit 2, skip 2
        resp2 = client.get("/jobs?skip=2&limit=2")
        assert resp2.status_code == 200
        page2 = resp2.json()
        assert len(page2) == 2

        # No overlap between page 1 and page 2
        page1_ids = {item["id"] for item in page1}
        page2_ids = {item["id"] for item in page2}
        assert page1_ids.isdisjoint(page2_ids)

    finally:
        for job in jobs:
            db_session.delete(job)
        db_session.delete(recruiter)
        db_session.delete(company)
        db_session.delete(user)
        db_session.commit()


def test_recruiter_jobs_pagination_and_ownership(db_session):
    # Recruiter A
    user_a = User(
        email=f"rec-a-{uuid4()}@example.com",
        password_hash=hash_password("Password123!"),
        role=UserRole.RECRUITER,
    )
    db_session.add(user_a)
    company = Company(name=f"Comp-{uuid4()}")
    db_session.add(company)
    db_session.commit()

    rec_a = Recruiter(user_id=user_a.id, company_id=company.id, first_name="A", last_name="Rec")
    db_session.add(rec_a)
    db_session.commit()

    # Recruiter B
    user_b = User(
        email=f"rec-b-{uuid4()}@example.com",
        password_hash=hash_password("Password123!"),
        role=UserRole.RECRUITER,
    )
    db_session.add(user_b)
    db_session.commit()
    rec_b = Recruiter(user_id=user_b.id, company_id=company.id, first_name="B", last_name="Rec")
    db_session.add(rec_b)
    db_session.commit()

    # 3 jobs for A, 1 job for B
    jobs_a = [
        Job(recruiter_id=rec_a.id, title=f"A Job {i}", description="Desc", location="Remote", employment_type="Full-time", experience_level="Mid")
        for i in range(3)
    ]
    job_b = Job(recruiter_id=rec_b.id, title="B Job", description="Desc", location="Remote", employment_type="Full-time", experience_level="Mid")

    for j in jobs_a:
        db_session.add(j)
    db_session.add(job_b)
    db_session.commit()

    token_a = create_access_token(user_id=str(user_a.id), role="recruiter")

    try:
        # Recruiter A lists jobs with limit 2
        resp = client.get("/recruiter/jobs?skip=0&limit=2", headers=auth_header(token_a))
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        # All returned jobs must belong to Recruiter A
        job_b_id = str(job_b.id)
        for item in data:
            assert item["id"] != job_b_id

        # Recruiter A lists second page
        resp_page2 = client.get("/recruiter/jobs?skip=2&limit=2", headers=auth_header(token_a))
        assert resp_page2.status_code == 200
        data_page2 = resp_page2.json()
        assert len(data_page2) == 1
        assert data_page2[0]["id"] != job_b_id

        # Parameter validation
        resp_invalid = client.get("/recruiter/jobs?limit=150", headers=auth_header(token_a))
        assert resp_invalid.status_code == 422

    finally:
        for j in jobs_a:
            db_session.delete(j)
        db_session.delete(job_b)
        db_session.delete(rec_a)
        db_session.delete(rec_b)
        db_session.delete(company)
        db_session.delete(user_a)
        db_session.delete(user_b)
        db_session.commit()


def test_candidate_applications_and_resumes_pagination(db_session):
    user = User(
        email=f"cand-page-{uuid4()}@example.com",
        password_hash=hash_password("Password123!"),
        role=UserRole.CANDIDATE,
    )
    db_session.add(user)
    db_session.commit()

    candidate = Candidate(
        user_id=user.id,
        first_name="Cand",
        last_name="Page",
        headline="Developer",
    )
    db_session.add(candidate)
    db_session.commit()

    # 3 resumes
    resumes = [
        Resume(
            candidate_id=candidate.id,
            original_filename=f"resume_{i}.pdf",
            file_path=f"/fake/path_{i}.pdf",
            parsing_status="COMPLETED",
        )
        for i in range(3)
    ]
    for r in resumes:
        db_session.add(r)
    db_session.commit()

    token = create_access_token(user_id=str(user.id), role="candidate")

    try:
        # GET /resumes with limit 2
        resp = client.get("/resumes?skip=0&limit=2", headers=auth_header(token))
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2

        # GET /resumes page 2
        resp2 = client.get("/resumes?skip=2&limit=2", headers=auth_header(token))
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert len(data2) == 1

        # Validation checks
        assert client.get("/resumes?limit=0", headers=auth_header(token)).status_code == 422
        assert client.get("/resumes?limit=101", headers=auth_header(token)).status_code == 422
        assert client.get("/resumes?skip=-5", headers=auth_header(token)).status_code == 422

        # GET /applications/me validation checks
        assert client.get("/applications/me?limit=0", headers=auth_header(token)).status_code == 422
        assert client.get("/applications/me?skip=0&limit=10", headers=auth_header(token)).status_code == 200

    finally:
        for r in resumes:
            db_session.delete(r)
        db_session.delete(candidate)
        db_session.delete(user)
        db_session.commit()
