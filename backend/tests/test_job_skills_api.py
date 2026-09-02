from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.models.recruiter import Recruiter
from app.models.skill import Skill
from app.models.user import User, UserRole


client = TestClient(app)


def test_recruiter_can_add_skill_to_own_job():
    db = SessionLocal()

    user = None
    recruiter = None
    job = None
    skill = None
    job_skill = None

    email = f"recruiter-api-job-skill-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary recruiter user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create recruiter profile
        # ---------------------------------------------------------
        recruiter = Recruiter(
            user_id=user.id,
            first_name="Test",
            last_name="Recruiter",
        )

        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        # ---------------------------------------------------------
        # Create temporary job owned by recruiter
        # ---------------------------------------------------------
        job = Job(
            recruiter_id=recruiter.id,
            title="Python Developer",
            description="Test job for JobSkill API.",
            location="India",
            employment_type="Full-time",
            experience_level="Mid",
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Add skill to job
        # ---------------------------------------------------------
        response = client.post(
            f"/jobs/{job.id}/skills",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "name": "Python",
                "is_required": True,
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert response.status_code == 201

        data = response.json()

        assert "skill_id" in data
        assert data["name"] == "Python"
        assert data["is_required"] is True

        # ---------------------------------------------------------
        # Verify database association
        # ---------------------------------------------------------
        skill = (
            db.query(Skill)
            .filter(Skill.id == data["skill_id"])
            .first()
        )

        assert skill is not None
        assert skill.name == "Python"

        job_skill = (
            db.query(JobSkill)
            .filter(
                JobSkill.job_id == job.id,
                JobSkill.skill_id == skill.id,
            )
            .first()
        )

        assert job_skill is not None
        assert job_skill.is_required is True

        print("Recruiter add-job-skill API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if job_skill:
            db.delete(job_skill)

        if skill:
            db.delete(skill)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary job-skill API data cleaned up.")


def test_recruiter_can_get_skills_for_own_job():
    db = SessionLocal()

    user = None
    recruiter = None
    job = None
    skill = None
    job_skill = None

    email = f"recruiter-api-get-job-skills-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary recruiter user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create recruiter profile
        # ---------------------------------------------------------
        recruiter = Recruiter(
            user_id=user.id,
            first_name="Test",
            last_name="Recruiter",
        )

        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        # ---------------------------------------------------------
        # Create temporary job
        # ---------------------------------------------------------
        job = Job(
            recruiter_id=recruiter.id,
            title="Python Developer",
            description="Test job for getting JobSkills.",
            location="India",
            employment_type="Full-time",
            experience_level="Mid",
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        # ---------------------------------------------------------
        # Create temporary skill
        # ---------------------------------------------------------
        skill = Skill(
            name=f"Python-{uuid4()}",
        )

        db.add(skill)
        db.commit()
        db.refresh(skill)

        # ---------------------------------------------------------
        # Create JobSkill association
        # ---------------------------------------------------------
        job_skill = JobSkill(
            job_id=job.id,
            skill_id=skill.id,
            is_required=True,
        )

        db.add(job_skill)
        db.commit()
        db.refresh(job_skill)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Get job skills
        # ---------------------------------------------------------
        response = client.get(
            f"/jobs/{job.id}/skills",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert response.status_code == 200

        data = response.json()

        assert isinstance(data, list)
        assert len(data) >= 1

        returned_skill = next(
            item
            for item in data
            if item["skill_id"] == str(skill.id)
        )

        assert returned_skill["name"] == skill.name
        assert returned_skill["is_required"] is True

        print("Recruiter get-job-skills API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if job_skill:
            db.delete(job_skill)

        if skill:
            db.delete(skill)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary get-job-skills data cleaned up.")


def test_recruiter_can_delete_skill_from_own_job():
    db = SessionLocal()

    user = None
    recruiter = None
    job = None
    skill = None
    job_skill = None

    email = f"recruiter-api-delete-job-skill-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary recruiter user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create recruiter profile
        # ---------------------------------------------------------
        recruiter = Recruiter(
            user_id=user.id,
            first_name="Test",
            last_name="Recruiter",
        )

        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        # ---------------------------------------------------------
        # Create temporary job
        # ---------------------------------------------------------
        job = Job(
            recruiter_id=recruiter.id,
            title="Python Developer",
            description="Test job for deleting JobSkill.",
            location="India",
            employment_type="Full-time",
            experience_level="Mid",
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        # ---------------------------------------------------------
        # Create temporary skill
        # ---------------------------------------------------------
        skill = Skill(
            name=f"Python-{uuid4()}",
        )

        db.add(skill)
        db.commit()
        db.refresh(skill)

        # ---------------------------------------------------------
        # Create JobSkill association
        # ---------------------------------------------------------
        job_skill = JobSkill(
            job_id=job.id,
            skill_id=skill.id,
            is_required=True,
        )

        db.add(job_skill)
        db.commit()
        db.refresh(job_skill)

        skill_id = str(skill.id)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Delete JobSkill
        # ---------------------------------------------------------
        response = client.delete(
            f"/jobs/{job.id}/skills/{skill_id}",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.text)

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert response.status_code == 204
        assert response.text == ""

        # ---------------------------------------------------------
        # Verify JobSkill association was deleted
        # ---------------------------------------------------------
        deleted_job_skill = (
            db.query(JobSkill)
            .filter(
                JobSkill.job_id == job.id,
                JobSkill.skill_id == skill.id,
            )
            .first()
        )

        assert deleted_job_skill is None

        # ---------------------------------------------------------
        # Verify shared Skill still exists
        # ---------------------------------------------------------
        remaining_skill = (
            db.query(Skill)
            .filter(Skill.id == skill.id)
            .first()
        )

        assert remaining_skill is not None
        assert remaining_skill.name == skill.name

        print("Recruiter delete-job-skill API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if job_skill:
            existing_job_skill = (
                db.query(JobSkill)
                .filter(
                    JobSkill.job_id == job.id,
                    JobSkill.skill_id == skill.id,
                )
                .first()
            )

            if existing_job_skill:
                db.delete(existing_job_skill)

        if skill:
            db.delete(skill)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary delete-job-skill data cleaned up.")


def test_recruiter_cannot_manage_another_recruiters_job_skills():
    db = SessionLocal()

    owner_user = None
    owner_recruiter = None
    other_user = None
    other_recruiter = None
    job = None
    skill = None
    job_skill = None

    owner_email = f"job-owner-{uuid4()}@example.com"
    other_email = f"other-recruiter-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create job owner
        # ---------------------------------------------------------
        owner_user = User(
            email=owner_email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        db.add(owner_user)
        db.commit()
        db.refresh(owner_user)

        owner_recruiter = Recruiter(
            user_id=owner_user.id,
            first_name="Owner",
            last_name="Recruiter",
        )

        db.add(owner_recruiter)
        db.commit()
        db.refresh(owner_recruiter)

        # ---------------------------------------------------------
        # Create job owned by first recruiter
        # ---------------------------------------------------------
        job = Job(
            recruiter_id=owner_recruiter.id,
            title="Python Developer",
            description="Job owned by another recruiter.",
            location="India",
            employment_type="Full-time",
            experience_level="Mid",
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        # ---------------------------------------------------------
        # Create another recruiter
        # ---------------------------------------------------------
        other_user = User(
            email=other_email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        db.add(other_user)
        db.commit()
        db.refresh(other_user)

        other_recruiter = Recruiter(
            user_id=other_user.id,
            first_name="Other",
            last_name="Recruiter",
        )

        db.add(other_recruiter)
        db.commit()
        db.refresh(other_recruiter)

        # ---------------------------------------------------------
        # Generate token for the OTHER recruiter
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(other_user.id),
            role=other_user.role.value,
        )

        # ---------------------------------------------------------
        # Try to add skill to someone else's job
        # ---------------------------------------------------------
        response = client.post(
            f"/jobs/{job.id}/skills",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "name": "Python",
                "is_required": True,
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert response.status_code == 403

        data = response.json()

        assert data["detail"] == (
            "You do not have permission to manage this job"
        )

        # ---------------------------------------------------------
        # Verify no JobSkill was created
        # ---------------------------------------------------------
        created_job_skills = (
            db.query(JobSkill)
            .filter(JobSkill.job_id == job.id)
            .all()
        )

        assert created_job_skills == []

        # ---------------------------------------------------------
        # Verify no Skill was created either
        # ---------------------------------------------------------
        skill = (
            db.query(Skill)
            .filter(Skill.name == "Python")
            .first()
        )

        # Python may already exist globally from another test,
        # so we don't assert that it doesn't exist.
        # The important assertion is that no JobSkill was created.

        print("Job ownership authorization test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if job_skill:
            db.delete(job_skill)

        if skill and skill.id:
            # Only delete the skill if it was created by this test.
            # Since "Python" may already exist globally, we leave it.
            pass

        if job:
            db.delete(job)

        if other_recruiter:
            db.delete(other_recruiter)

        if other_user:
            db.delete(other_user)

        if owner_recruiter:
            db.delete(owner_recruiter)

        if owner_user:
            db.delete(owner_user)

        db.commit()
        db.close()

        print("Temporary job ownership test data cleaned up.")


def test_recruiter_cannot_add_duplicate_skill_to_own_job():
    db = SessionLocal()

    user = None
    recruiter = None
    job = None
    skill = None
    job_skill = None

    email = f"recruiter-api-duplicate-job-skill-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary recruiter user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.RECRUITER,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create recruiter profile
        # ---------------------------------------------------------
        recruiter = Recruiter(
            user_id=user.id,
            first_name="Test",
            last_name="Recruiter",
        )

        db.add(recruiter)
        db.commit()
        db.refresh(recruiter)

        # ---------------------------------------------------------
        # Create temporary job owned by recruiter
        # ---------------------------------------------------------
        job = Job(
            recruiter_id=recruiter.id,
            title="Python Developer",
            description="Test job for duplicate JobSkill API.",
            location="India",
            employment_type="Full-time",
            experience_level="Mid",
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Add skill to job for the first time
        # ---------------------------------------------------------
        first_response = client.post(
            f"/jobs/{job.id}/skills",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "name": "Python",
                "is_required": True,
            },
        )

        print("First Status:", first_response.status_code)
        print("First Response:", first_response.json())

        assert first_response.status_code == 201

        first_data = first_response.json()

        skill_id = first_data["skill_id"]

        # ---------------------------------------------------------
        # Verify JobSkill was created
        # ---------------------------------------------------------
        skill = (
            db.query(Skill)
            .filter(Skill.id == skill_id)
            .first()
        )

        assert skill is not None
        assert skill.name == "Python"

        job_skill = (
            db.query(JobSkill)
            .filter(
                JobSkill.job_id == job.id,
                JobSkill.skill_id == skill.id,
            )
            .first()
        )

        assert job_skill is not None

        # ---------------------------------------------------------
        # Try to add the SAME skill again
        # ---------------------------------------------------------
        duplicate_response = client.post(
            f"/jobs/{job.id}/skills",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "name": "Python",
                "is_required": True,
            },
        )

        print(
            "Duplicate Status:",
            duplicate_response.status_code,
        )
        print(
            "Duplicate Response:",
            duplicate_response.json(),
        )

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert duplicate_response.status_code == 409

        assert duplicate_response.json()["detail"] == (
            "Skill already added to job"
        )

        # ---------------------------------------------------------
        # Verify only ONE JobSkill association exists
        # ---------------------------------------------------------
        job_skills = (
            db.query(JobSkill)
            .filter(JobSkill.job_id == job.id)
            .all()
        )

        assert len(job_skills) == 1
        assert job_skills[0].skill_id == skill.id

        print("Recruiter duplicate-job-skill API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if job_skill:
            existing_job_skill = (
                db.query(JobSkill)
                .filter(
                    JobSkill.job_id == job.id,
                    JobSkill.skill_id == skill.id,
                )
                .first()
            )

            if existing_job_skill:
                db.delete(existing_job_skill)

        if skill:
            db.delete(skill)

        if job:
            db.delete(job)

        if recruiter:
            db.delete(recruiter)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary duplicate-job-skill data cleaned up.")