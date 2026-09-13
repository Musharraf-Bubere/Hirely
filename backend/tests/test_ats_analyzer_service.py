from uuid import uuid4

from app.ai.ats_analyzer.analyzer import ATSDeterministicResult
from app.ai.ats_analyzer.service import ATSAnalyzerService
from app.ai.ats_analyzer.schemas import ATSAnalysisResult


def test_generate_analysis_orchestrates_ats_pipeline(monkeypatch):
    service = ATSAnalyzerService()

    candidate_id = uuid4()
    job_id = uuid4()

    candidate = type(
        "Candidate",
        (),
        {
            "id": candidate_id,
            "first_name": "John",
            "last_name": "Doe",
            "headline": "Python Developer",
            "bio": "Backend developer with Python experience.",
            "location": "Mumbai",
            "candidate_skills": [],
        },
    )()

    job = type(
        "Job",
        (),
        {
            "id": job_id,
            "title": "Python Backend Developer",
            "description": "Build backend APIs using Python and FastAPI.",
            "location": "Mumbai",
            "employment_type": "Full-time",
            "experience_level": "Mid-level",
            "job_skills": [],
        },
    )()

    deterministic_result = ATSDeterministicResult(
        required_skill_score=0.8,
        preferred_skill_score=0.5,
        resume_completeness_score=0.9,
        required_skills_matched=["Python", "FastAPI"],
        required_skills_missing=["PostgreSQL"],
        preferred_skills_matched=["Docker"],
        preferred_skills_missing=["AWS"],
    )

    ai_result = ATSAnalysisResult(
        ats_score=0,
        score_breakdown={
            "required_skill_score": 0.0,
            "preferred_skill_score": 0.0,
            "semantic_relevance_score": 0.0,
            "resume_completeness_score": 0.0,
        },
        required_skills_matched=[],
        required_skills_missing=[],
        preferred_skills_matched=[],
        preferred_skills_missing=[],
        strengths=[
            "Strong Python and FastAPI experience.",
        ],
        improvement_areas=[
            "Add PostgreSQL experience.",
        ],
        suggestions=[
            "Highlight backend API projects.",
        ],
        summary="The resume is a strong match with some areas for improvement.",
    )

    monkeypatch.setattr(
        service,
        "build_context",
        lambda db, candidate, job: object(),
    )

    monkeypatch.setattr(
        service.analyzer,
        "analyze",
        lambda context: deterministic_result,
    )

    monkeypatch.setattr(
        service.semantic_analyzer,
        "calculate",
        lambda context: 0.7,
    )

    monkeypatch.setattr(
        service.prompt_builder,
        "build",
        lambda context: "ATS analysis prompt",
    )

    def mock_generate_structured(*, prompt, response_schema):
        assert prompt == "ATS analysis prompt"
        assert response_schema is ATSAnalysisResult
        return ai_result

    monkeypatch.setattr(
        service.gemini_service,
        "generate_structured",
        mock_generate_structured,
    )

    response = service.generate_analysis(
        db=None,
        candidate=candidate,
        job=job,
    )

    expected_score = round(
        (
            0.8 * 0.45
            + 0.5 * 0.15
            + 0.7 * 0.30
            + 0.9 * 0.10
        )
        * 100
    )

    assert response.job_id == job_id

    assert response.ats_analysis.ats_score == expected_score

    assert (
        response.ats_analysis.score_breakdown.required_skill_score
        == 0.8
    )
    assert (
        response.ats_analysis.score_breakdown.preferred_skill_score
        == 0.5
    )
    assert (
        response.ats_analysis.score_breakdown.semantic_relevance_score
        == 0.7
    )
    assert (
        response.ats_analysis.score_breakdown.resume_completeness_score
        == 0.9
    )

    assert response.ats_analysis.required_skills_matched == [
        "Python",
        "FastAPI",
    ]
    assert response.ats_analysis.required_skills_missing == [
        "PostgreSQL",
    ]

    assert response.ats_analysis.preferred_skills_matched == [
        "Docker",
    ]
    assert response.ats_analysis.preferred_skills_missing == [
        "AWS",
    ]

    assert response.ats_analysis.strengths == [
        "Strong Python and FastAPI experience.",
    ]
    assert response.ats_analysis.improvement_areas == [
        "Add PostgreSQL experience.",
    ]
    assert response.ats_analysis.suggestions == [
        "Highlight backend API projects.",
    ]
    assert (
        response.ats_analysis.summary
        == "The resume is a strong match with some areas for improvement."
    )


def test_calculate_ats_score_uses_expected_weights():
    service = ATSAnalyzerService()

    score = service._calculate_ats_score(
        required_skill_score=1.0,
        preferred_skill_score=1.0,
        semantic_relevance_score=1.0,
        resume_completeness_score=1.0,
    )

    assert score == 100


def test_calculate_ats_score_rounds_to_nearest_integer():
    service = ATSAnalyzerService()

    score = service._calculate_ats_score(
        required_skill_score=0.81,
        preferred_skill_score=0.52,
        semantic_relevance_score=0.73,
        resume_completeness_score=0.91,
    )

    expected = round(
        (
            0.81 * 0.45
            + 0.52 * 0.15
            + 0.73 * 0.30
            + 0.91 * 0.10
        )
        * 100
    )

    assert score == expected