from uuid import uuid4

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.models.recruiter import Recruiter
from app.models.skill import Skill
from app.models.user import User, UserRole
from app.services.job_skill import add_job_skill


def test_add_job_skill():
    db = SessionLocal()

    user = None
    recruiter = None
    job = None
    skill = None
    job_skill = None

    email = f"job-skill-{uuid4()}@example.com"

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
            description="Test job for JobSkill service.",
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
        # Add skill to job
        # ---------------------------------------------------------
        job_skill = add_job_skill(
            db=db,
            job=job,
            skill=skill,
            is_required=True,
        )

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert job_skill is not None
        assert job_skill.job_id == job.id
        assert job_skill.skill_id == skill.id
        assert job_skill.is_required is True

        # ---------------------------------------------------------
        # Verify association exists in database
        # ---------------------------------------------------------
        saved_association = (
            db.query(JobSkill)
            .filter(
                JobSkill.job_id == job.id,
                JobSkill.skill_id == skill.id,
            )
            .first()
        )

        assert saved_association is not None
        assert saved_association.is_required is True

        print("Job skill service test passed.")

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

        print("Temporary job skill data cleaned up.")


def test_add_duplicate_job_skill():
    db = SessionLocal()

    user = None
    recruiter = None
    job = None
    skill = None
    job_skill = None

    email = f"job-duplicate-skill-{uuid4()}@example.com"

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
            description="Test job for duplicate JobSkill.",
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
        # Add skill for the first time
        # ---------------------------------------------------------
        job_skill = add_job_skill(
            db=db,
            job=job,
            skill=skill,
            is_required=True,
        )

        assert job_skill is not None

        # ---------------------------------------------------------
        # Try adding the same skill again
        # Expected: ValueError
        # ---------------------------------------------------------
        try:
            add_job_skill(
                db=db,
                job=job,
                skill=skill,
                is_required=False,
            )

            assert False, "Expected ValueError was not raised"

        except ValueError as exc:
            assert str(exc) == "Skill already added to job"

        print("Duplicate job skill test passed.")

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

        print("Temporary duplicate job skill data cleaned up.")