from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.candidate_skill import CandidateSkill
from app.models.skill import Skill
from app.models.user import User, UserRole


client = TestClient(app)


def test_candidate_can_add_skill():
    db = SessionLocal()

    user = None
    candidate = None
    skill_id = None

    email = f"candidate-api-skill-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary candidate user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create candidate profile
        # ---------------------------------------------------------
        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Add skill
        # ---------------------------------------------------------
        response = client.post(
            "/candidate/skills",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "name": "Python",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert response.status_code == 201

        data = response.json()

        assert "id" in data
        assert data["name"] == "Python"

        skill_id = data["id"]

        print("Candidate add-skill API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if skill_id:
            from app.models.candidate_skill import CandidateSkill
            from app.models.skill import Skill

            skill = db.query(Skill).filter(Skill.id == skill_id).first()

            if skill:
                association = (
                    db.query(CandidateSkill)
                    .filter(CandidateSkill.skill_id == skill.id)
                    .first()
                )

                if association:
                    db.delete(association)

                db.delete(skill)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary candidate API skill data cleaned up.")


def test_candidate_can_get_skills():
    db = SessionLocal()

    user = None
    candidate = None
    skill = None
    candidate_skill = None

    email = f"candidate-api-get-skills-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary candidate user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create candidate profile
        # ---------------------------------------------------------
        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create skill
        # ---------------------------------------------------------
        skill = Skill(
            name=f"Python-{uuid4()}",
        )

        db.add(skill)
        db.commit()
        db.refresh(skill)

        # ---------------------------------------------------------
        # Create candidate-skill association
        # ---------------------------------------------------------
        candidate_skill = CandidateSkill(
            candidate_id=candidate.id,
            skill_id=skill.id,
        )

        db.add(candidate_skill)
        db.commit()
        db.refresh(candidate_skill)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Get candidate skills
        # ---------------------------------------------------------
        response = client.get(
            "/candidate/skills",
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
            item for item in data
            if item["id"] == str(skill.id)
        )

        assert returned_skill["name"] == skill.name

        print("Candidate get-skills API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if candidate_skill:
            db.delete(candidate_skill)

        if skill:
            db.delete(skill)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary candidate get-skills data cleaned up.")


def test_candidate_can_delete_skill():
    db = SessionLocal()

    user = None
    candidate = None
    skill = None
    candidate_skill = None

    email = f"candidate-api-delete-skill-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary candidate user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create candidate profile
        # ---------------------------------------------------------
        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create skill
        # ---------------------------------------------------------
        skill = Skill(
            name=f"Python-{uuid4()}",
        )

        db.add(skill)
        db.commit()
        db.refresh(skill)

        # ---------------------------------------------------------
        # Create candidate-skill association
        # ---------------------------------------------------------
        candidate_skill = CandidateSkill(
            candidate_id=candidate.id,
            skill_id=skill.id,
        )

        db.add(candidate_skill)
        db.commit()
        db.refresh(candidate_skill)

        skill_id = str(skill.id)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Delete candidate skill
        # ---------------------------------------------------------
        response = client.delete(
            f"/candidate/skills/{skill_id}",
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
        # Verify association was deleted
        # ---------------------------------------------------------
        deleted_association = (
            db.query(CandidateSkill)
            .filter(
                CandidateSkill.candidate_id == candidate.id,
                CandidateSkill.skill_id == skill.id,
            )
            .first()
        )

        assert deleted_association is None

        # ---------------------------------------------------------
        # Verify Skill itself still exists
        # ---------------------------------------------------------
        remaining_skill = (
            db.query(Skill)
            .filter(Skill.id == skill.id)
            .first()
        )

        assert remaining_skill is not None
        assert remaining_skill.name == skill.name

        print("Candidate delete-skill API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if candidate_skill:
            existing_association = (
                db.query(CandidateSkill)
                .filter(
                    CandidateSkill.candidate_id == candidate.id,
                    CandidateSkill.skill_id == skill.id,
                )
                .first()
            )

            if existing_association:
                db.delete(existing_association)

        if skill:
            db.delete(skill)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary candidate delete-skill data cleaned up.")


def test_candidate_cannot_add_duplicate_skill():
    db = SessionLocal()

    user = None
    candidate = None
    skill = None
    candidate_skill = None

    email = f"candidate-api-duplicate-skill-{uuid4()}@example.com"

    try:
        # ---------------------------------------------------------
        # Create temporary candidate user
        # ---------------------------------------------------------
        user = User(
            email=email,
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # ---------------------------------------------------------
        # Create candidate profile
        # ---------------------------------------------------------
        candidate = Candidate(
            user_id=user.id,
            first_name="Test",
            last_name="Candidate",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        # ---------------------------------------------------------
        # Create skill
        # ---------------------------------------------------------
        skill = Skill(
            name=f"Python-{uuid4()}",
        )

        db.add(skill)
        db.commit()
        db.refresh(skill)

        # ---------------------------------------------------------
        # Create existing candidate-skill association
        # ---------------------------------------------------------
        candidate_skill = CandidateSkill(
            candidate_id=candidate.id,
            skill_id=skill.id,
        )

        db.add(candidate_skill)
        db.commit()
        db.refresh(candidate_skill)

        # ---------------------------------------------------------
        # Generate access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Try adding the same skill again
        # ---------------------------------------------------------
        response = client.post(
            "/candidate/skills",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "name": skill.name,
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert response.status_code == 409

        data = response.json()

        assert data["detail"] == "Skill already added to candidate"

        print("Candidate duplicate-skill API test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if candidate_skill:
            existing_association = (
                db.query(CandidateSkill)
                .filter(
                    CandidateSkill.candidate_id == candidate.id,
                    CandidateSkill.skill_id == skill.id,
                )
                .first()
            )

            if existing_association:
                db.delete(existing_association)

        if skill:
            db.delete(skill)

        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary duplicate-skill API data cleaned up.")


def test_recruiter_cannot_manage_candidate_skills():
    db = SessionLocal()

    user = None

    email = f"recruiter-api-candidate-skills-{uuid4()}@example.com"

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
        # Generate recruiter access token
        # ---------------------------------------------------------
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        # ---------------------------------------------------------
        # Try to add candidate skill
        # ---------------------------------------------------------
        response = client.post(
            "/candidate/skills",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json={
                "name": "Python",
            },
        )

        print("Status:", response.status_code)
        print("Response:", response.json())

        # ---------------------------------------------------------
        # Assertions
        # ---------------------------------------------------------
        assert response.status_code == 403

        print("Recruiter RBAC candidate-skills test passed.")

    finally:
        # ---------------------------------------------------------
        # Cleanup
        # ---------------------------------------------------------
        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary recruiter data cleaned up.")