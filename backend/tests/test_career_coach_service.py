from uuid import uuid4

from app.ai.career_coach.schemas import CareerCoachRequest, CareerCoachResponse
from app.ai.career_coach.service import career_coach_service
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.candidate import Candidate
from app.models.user import User, UserRole


def test_career_coach_works_without_active_resume(monkeypatch):
    db = SessionLocal()

    user = None
    candidate = None

    expected_response = CareerCoachResponse(
        answer=(
            "You can continue improving your career profile using your "
            "current profile and skills even without an active resume."
        ),
        recommendations=[
            "Strengthen your technical skills through practical projects.",
            "Keep your candidate profile updated.",
        ],
        skills_to_improve=[
            "Machine Learning",
            "FastAPI",
        ],
        next_steps=[
            "Build a practical AI project.",
            "Add your completed projects and skills to your profile.",
        ],
    )

    try:
        user = User(
            email=f"career-coach-no-resume-{uuid4()}@example.com",
            password_hash=hash_password("TestPassword123!"),
            role=UserRole.CANDIDATE,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        candidate = Candidate(
            user_id=user.id,
            first_name="No",
            last_name="Resume",
            headline="Python Developer",
            bio="Backend developer building Python applications.",
            location="India",
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        context = career_coach_service.build_context(
            db=db,
            candidate=candidate,
        )

        assert context.resume is None
        assert context.name == "No Resume"

        captured_prompt = {}

        def mock_generate_structured(prompt, response_schema):
            captured_prompt["prompt"] = prompt
            captured_prompt["response_schema"] = response_schema

            return expected_response

        monkeypatch.setattr(
            career_coach_service.gemini_service,
            "generate_structured",
            mock_generate_structured,
        )

        request = CareerCoachRequest(
            message="What should I learn next for my career?"
        )

        response = career_coach_service.generate_response(
            db=db,
            candidate=candidate,
            request=request,
        )

        assert response == expected_response
        assert captured_prompt["response_schema"] is CareerCoachResponse
        assert "No Resume" in captured_prompt["prompt"]
        assert "What should I learn next for my career?" in captured_prompt["prompt"]

        print("Career Coach without active resume test passed.")

    finally:
        if candidate:
            db.delete(candidate)

        if user:
            db.delete(user)

        db.commit()
        db.close()

        print("Temporary no-resume test data cleaned up.")