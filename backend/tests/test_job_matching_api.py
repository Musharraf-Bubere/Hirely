import pytest
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app

from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.resume import Resume
from app.models.user import User, UserRole
from app.models.skill import Skill
from app.models.candidate_skill import CandidateSkill
from app.models.job_skill import JobSkill


client = TestClient(app)


@pytest.mark.integration
def test_candidate_can_match_active_resume_to_active_job():
    db = SessionLocal()

    candidate_user = None
    candidate = None
    recruiter_user = None
    recruiter = None
    job = None
    resume = None

    candidate_skills = []
    job_skills = []

    try:
        # ---------------------------------------------------------
        # Create candidate user
        # ---------------------------------------------------------
        candidate_user = User(
            email=f"matching-candidate-{uuid4()}@example.com",
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(candidate_user)
        db.commit()
        db.refresh(candidate_user)

        # ---------------------------------------------------------
        # Create candidate profile
        # ---------------------------------------------------------
        candidate = Candidate(
            user_id=candidate_user.id,
            first_name="Test",
            last_name="Candidate",
            headline="Python Backend Developer",
            bio="Backend developer with Python and FastAPI experience.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create recruiter user
        # ---------------------------------------------------------
        recruiter_user = User(
            email=f"matching-recruiter-{uuid4()}@example.com",
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        db.add(recruiter_user)
        db.commit()
        db.refresh(recruiter_user)

        # ---------------------------------------------------------
        # Create recruiter profile
        # ---------------------------------------------------------
        recruiter = Recruiter(
            user_id=recruiter_user.id,
            first_name="Test",
            last_name="Recruiter",
            job_title="Talent Acquisition Specialist",
            location="India",
        )

        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        # ---------------------------------------------------------
        # Create active job
        # ---------------------------------------------------------
        job = Job(
            recruiter_id=recruiter.id,
            title="Python Backend Developer",
            description=(
                "Build scalable backend APIs using Python and FastAPI. "
                "Work with SQL databases and REST APIs."
            ),
            location="India",
            employment_type="full_time",
            experience_level="mid",
            is_active=True,
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        # ---------------------------------------------------------
        # Create candidate skills
        # ---------------------------------------------------------
        python_skill = Skill(name=f"Python-{uuid4()}")
        fastapi_skill = Skill(name=f"FastAPI-{uuid4()}")
        sql_skill = Skill(name=f"SQL-{uuid4()}")

        db.add_all([
            python_skill,
            fastapi_skill,
            sql_skill,
        ])
        db.commit()

        db.refresh(python_skill)
        db.refresh(fastapi_skill)
        db.refresh(sql_skill)

        candidate_skills = [
            CandidateSkill(
                candidate_id=candidate.id,
                skill_id=python_skill.id,
            ),
            CandidateSkill(
                candidate_id=candidate.id,
                skill_id=fastapi_skill.id,
            ),
            CandidateSkill(
                candidate_id=candidate.id,
                skill_id=sql_skill.id,
            ),
        ]

        db.add_all(candidate_skills)
        db.commit()

        # ---------------------------------------------------------
        # Create job skills
        # ---------------------------------------------------------
        job_skills = [
            JobSkill(
                job_id=job.id,
                skill_id=python_skill.id,
                is_required=True,
            ),
            JobSkill(
                job_id=job.id,
                skill_id=fastapi_skill.id,
                is_required=True,
            ),
            JobSkill(
                job_id=job.id,
                skill_id=sql_skill.id,
                is_required=False,
            ),
        ]

        db.add_all(job_skills)
        db.commit()

        # ---------------------------------------------------------
        # Create active + completed resume
        # ---------------------------------------------------------
        resume = Resume(
            candidate_id=candidate.id,
            original_filename="matching_test_resume.pdf",
            file_path="test_data/matching_test_resume.pdf",
            parsing_status="COMPLETED",
            is_active=True,
            parsed_data={
                "name": "Test Candidate",
                "email": candidate_user.email,
                "phone": None,
                "location": "India",
                "headline": "Python Backend Developer",
                "summary": (
                    "Backend developer experienced in Python, "
                    "FastAPI, SQL and REST APIs."
                ),
                "skills": [
                    "Python",
                    "FastAPI",
                    "SQL",
                ],
                "experience": [
                    {
                        "company": "Hirely Test Company",
                        "job_title": "Python Developer",
                        "start_date": "2024",
                        "end_date": "2026",
                        "description": (
                            "Developed backend APIs using Python "
                            "and FastAPI."
                        ),
                    }
                ],
                "projects": [],
                "education": [],
                "certifications": [],
            },
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # ---------------------------------------------------------
        # Generate candidate JWT
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(candidate_user.id),
            role=candidate_user.role.value,
        )

        # ---------------------------------------------------------
        # Call matching API
        # ---------------------------------------------------------
        response = client.post(
            f"/jobs/{job.id}/match",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Candidate → Match Job:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert response.status_code == 200

        data = response.json()

        assert "score" in data
        assert "skills" in data

        score = data["score"]
        skills = data["skills"]

        assert score["candidate_id"] == str(candidate.id)

        assert 0.0 <= score["overall_score"] <= 1.0
        assert 0.0 <= score["required_skill_score"] <= 1.0
        assert 0.0 <= score["semantic_similarity"] <= 1.0

        assert "required_matched" in skills
        assert "required_missing" in skills
        assert "preferred_matched" in skills
        assert "preferred_missing" in skills

        print("Candidate → Job matching API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup associations first
        # ---------------------------------------------------------
        if candidate_skills:
            for item in candidate_skills:
                db.delete(item)

        if job_skills:
            for item in job_skills:
                db.delete(item)

        db.commit()

        # ---------------------------------------------------------
        # Cleanup resume
        # ---------------------------------------------------------
        if resume:
            db.delete(resume)

        # ---------------------------------------------------------
        # Cleanup job
        # ---------------------------------------------------------
        if job:
            db.delete(job)

        # ---------------------------------------------------------
        # Cleanup recruiter
        # ---------------------------------------------------------
        if recruiter:
            db.delete(recruiter)

        if recruiter_user:
            db.delete(recruiter_user)

        # ---------------------------------------------------------
        # Cleanup candidate
        # ---------------------------------------------------------
        if candidate:
            db.delete(candidate)

        if candidate_user:
            db.delete(candidate_user)

        # ---------------------------------------------------------
        # Cleanup skills
        # ---------------------------------------------------------
        for skill in [
            locals().get("python_skill"),
            locals().get("fastapi_skill"),
            locals().get("sql_skill"),
        ]:
            if skill:
                db.delete(skill)

        db.commit()
        db.close()

        print("Temporary matching API data cleaned up.")

# =========================================================
# NEGATIVE CASES
# =========================================================

import pytest
from uuid import uuid4

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.resume import Resume
from app.models.user import User, UserRole


def test_match_requires_active_resume():
    db = SessionLocal()

    user = None
    candidate = None
    recruiter_user = None
    recruiter = None
    job = None

    try:
        user = User(
            email=f"no-resume-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.CANDIDATE,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        recruiter_user = User(
            email=f"recruiter-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.RECRUITER,
        )
        db.add(recruiter_user)
        db.commit()
        db.refresh(recruiter_user)

        recruiter = Recruiter(
            user_id=recruiter_user.id,
            first_name="Test",
            last_name="Recruiter",
        )
        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        job = Job(
            recruiter_id=recruiter.id,
            title="Python Developer",
            description="Backend role",
            employment_type="FULL_TIME",
            is_active=True,
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        response = client.post(
            f"/jobs/{job.id}/match",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Active resume not found"

    finally:
        if job:
            db.delete(job)
        if recruiter:
            db.delete(recruiter)
        if recruiter_user:
            db.delete(recruiter_user)
        if candidate:
            db.delete(candidate)
        if user:
            db.delete(user)
        db.commit()
        db.close()


def test_match_requires_completed_resume():
    db = SessionLocal()

    user = None
    candidate = None
    recruiter_user = None
    recruiter = None
    job = None
    resume = None

    try:
        user = User(
            email=f"pending-resume-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.CANDIDATE,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        resume = Resume(
            candidate_id=candidate.id,
            original_filename="resume.pdf",
            file_path="test.pdf",
            parsing_status="PENDING",
            is_active=True,
        )
        db.add(resume)
        db.commit()

        recruiter_user = User(
            email=f"recruiter-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.RECRUITER,
        )
        db.add(recruiter_user)
        db.commit()
        db.refresh(recruiter_user)

        recruiter = Recruiter(
            user_id=recruiter_user.id,
            first_name="Test",
            last_name="Recruiter",
        )
        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        job = Job(
            recruiter_id=recruiter.id,
            title="Python Developer",
            description="Backend role",
            employment_type="FULL_TIME",
            is_active=True,
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        response = client.post(
            f"/jobs/{job.id}/match",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Active resume has not been parsed"

    finally:
        if resume:
            db.delete(resume)
        if job:
            db.delete(job)
        if recruiter:
            db.delete(recruiter)
        if recruiter_user:
            db.delete(recruiter_user)
        if candidate:
            db.delete(candidate)
        if user:
            db.delete(user)
        db.commit()
        db.close()


def test_match_rejects_inactive_job():
    db = SessionLocal()

    user = None
    candidate = None
    recruiter_user = None
    recruiter = None
    job = None
    resume = None

    try:
        user = User(
            email=f"inactive-job-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.CANDIDATE,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        resume = Resume(
            candidate_id=candidate.id,
            original_filename="resume.pdf",
            file_path="resume.pdf",
            parsing_status="COMPLETED",
            is_active=True,
            parsed_data={
                "name": "Test",
                "email": "test@example.com",
                "skills": ["Python"],
            },
        )
        db.add(resume)
        db.commit()

        recruiter_user = User(
            email=f"recruiter-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.RECRUITER,
        )
        db.add(recruiter_user)
        db.commit()
        db.refresh(recruiter_user)

        recruiter = Recruiter(
            user_id=recruiter_user.id,
            first_name="Test",
            last_name="Recruiter",
        )
        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        job = Job(
            recruiter_id=recruiter.id,
            title="Python Developer",
            description="Backend role",
            employment_type="FULL_TIME",
            is_active=False,
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        response = client.post(
            f"/jobs/{job.id}/match",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"

    finally:
        if resume:
            db.delete(resume)
        if job:
            db.delete(job)
        if recruiter:
            db.delete(recruiter)
        if recruiter_user:
            db.delete(recruiter_user)
        if candidate:
            db.delete(candidate)
        if user:
            db.delete(user)
        db.commit()
        db.close()


def test_match_returns_404_for_unknown_job():
    db = SessionLocal()

    user = None
    candidate = None

    try:
        user = User(
            email=f"unknown-job-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.CANDIDATE,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )
        db.add(candidate)
        db.commit()

        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        response = client.post(
            f"/jobs/{uuid4()}/match",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404

    finally:
        if candidate:
            db.delete(candidate)
        if user:
            db.delete(user)
        db.commit()
        db.close()


def test_recruiter_cannot_match_jobs():
    db = SessionLocal()

    recruiter_user = None

    try:
        recruiter_user = User(
            email=f"recruiter-only-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.RECRUITER,
        )
        db.add(recruiter_user)
        db.commit()
        db.refresh(recruiter_user)

        token = create_access_token(
            user_id=str(recruiter_user.id),
            role=recruiter_user.role.value,
        )

        response = client.post(
            f"/jobs/{uuid4()}/match",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 403

    finally:
        if recruiter_user:
            db.delete(recruiter_user)
        db.commit()
        db.close()


def test_match_requires_authentication():
    response = client.post(
        f"/jobs/{uuid4()}/match",
    )

    assert response.status_code == 401