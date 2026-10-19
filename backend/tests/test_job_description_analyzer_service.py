from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.ai.job_description_analyzer.schemas import (
    IssueCategory,
    IssuePriority,
    JobDescriptionAIResult,
    JobDescriptionAnalysisResponse,
    JobDescriptionIssue,
    JobSkillsAnalysis,
)
from app.ai.job_description_analyzer.service import (
    JobDescriptionAnalyzerService,
)
from app.models.job import Job
from app.models.job_skill import JobSkill
from app.models.recruiter import Recruiter
from app.models.skill import Skill


def make_mock_ai_result() -> JobDescriptionAIResult:
    return JobDescriptionAIResult(
        quality_score=82,
        overall_assessment="Clear technical scope and strong responsibility definition.",
        strengths=["Clear requirements.", "Explicit tech stack."],
        issues=[
            JobDescriptionIssue(
                priority=IssuePriority.MEDIUM,
                category=IssueCategory.COMPLETENESS,
                title="Missing office location details",
                explanation="Job states Bengaluru but does not mention office zone.",
                suggested_action="Specify office area or hybrid schedule.",
            )
        ],
        missing_information=["Interview process stages."],
        skills_analysis=JobSkillsAnalysis(
            required_skills_evaluation="Python and FastAPI are well aligned.",
            preferred_skills_evaluation="PostgreSQL is mentioned appropriately.",
            unmentioned_skills_in_description=[],
            suggested_skills_to_add=["Docker"],
        ),
        improvement_recommendations=["Add 2-3 bullets on engineering team culture."],
        improved_description="Optimized job description with [Placeholders].",
    )


def test_service_orchestration_success():
    recruiter_id = uuid4()
    job_id = uuid4()

    recruiter = Recruiter(
        id=recruiter_id,
        user_id=uuid4(),
        first_name="Jane",
        last_name="Recruiter",
    )

    skill_py = Skill(id=uuid4(), name="Python")
    skill_fastapi = Skill(id=uuid4(), name="FastAPI")
    skill_docker = Skill(id=uuid4(), name="Docker")

    job = Job(
        id=job_id,
        recruiter_id=recruiter_id,
        title="Lead Python Developer",
        description="Lead our backend team building real-time recruitment engines with Python and FastAPI.",
        location="Bengaluru",
        employment_type="Full-time",
        experience_level="Senior",
        salary_min=1800000,
        salary_max=2800000,
        is_active=True,
    )
    job.job_skills = [
        JobSkill(job_id=job_id, skill_id=skill_py.id, is_required=True, skill=skill_py),
        JobSkill(job_id=job_id, skill_id=skill_fastapi.id, is_required=True, skill=skill_fastapi),
        JobSkill(job_id=job_id, skill_id=skill_docker.id, is_required=False, skill=skill_docker),
    ]

    service = JobDescriptionAnalyzerService()
    mock_gemini = MagicMock()
    mock_gemini.generate_structured.return_value = make_mock_ai_result()
    service.gemini_service = mock_gemini

    db_mock = MagicMock()

    response = service.analyze_job_description(
        db=db_mock,
        recruiter=recruiter,
        job=job,
    )

    assert isinstance(response, JobDescriptionAnalysisResponse)
    assert response.job_id == job_id
    assert response.analysis.quality_score == 82
    assert "heuristic evaluation" in response.analysis.disclaimer
    assert len(response.analysis.strengths) == 2
    assert len(response.analysis.issues) == 1
    assert response.analysis.issues[0].priority == IssuePriority.MEDIUM

    # Verify Gemini was invoked with prompt containing skills
    mock_gemini.generate_structured.assert_called_once()
    call_args = mock_gemini.generate_structured.call_args
    prompt_used = call_args.kwargs["prompt"]
    assert "Lead Python Developer" in prompt_used
    assert "FastAPI, Python" in prompt_used
    assert "Docker" in prompt_used


def test_service_ownership_mismatch_raises_value_error():
    recruiter = Recruiter(
        id=uuid4(),
        user_id=uuid4(),
        first_name="Authorized",
        last_name="Recruiter",
    )

    other_recruiter_id = uuid4()
    job = Job(
        id=uuid4(),
        recruiter_id=other_recruiter_id,
        title="Unauthorized Job",
        description="Should not be analyzable by another recruiter.",
        employment_type="Full-time",
    )

    service = JobDescriptionAnalyzerService()
    db_mock = MagicMock()

    with pytest.raises(ValueError, match="do not have permission"):
        service.analyze_job_description(
            db=db_mock,
            recruiter=recruiter,
            job=job,
        )


def test_service_empty_description_raises_value_error():
    recruiter_id = uuid4()
    recruiter = Recruiter(
        id=recruiter_id,
        user_id=uuid4(),
        first_name="Jane",
        last_name="Recruiter",
    )

    job = Job(
        id=uuid4(),
        recruiter_id=recruiter_id,
        title="Empty Description Job",
        description="   ",
        employment_type="Full-time",
    )

    service = JobDescriptionAnalyzerService()
    db_mock = MagicMock()

    with pytest.raises(ValueError, match="description cannot be empty"):
        service.analyze_job_description(
            db=db_mock,
            recruiter=recruiter,
            job=job,
        )


def test_service_gemini_error_propagates():
    recruiter_id = uuid4()
    recruiter = Recruiter(
        id=recruiter_id,
        user_id=uuid4(),
    )

    job = Job(
        id=uuid4(),
        recruiter_id=recruiter_id,
        title="Python Dev",
        description="Valid description.",
        employment_type="Full-time",
    )
    job.job_skills = []

    service = JobDescriptionAnalyzerService()
    mock_gemini = MagicMock()
    mock_gemini.generate_structured.side_effect = RuntimeError("Gemini upstream 503")
    service.gemini_service = mock_gemini

    db_mock = MagicMock()

    with pytest.raises(RuntimeError, match="Gemini upstream 503"):
        service.analyze_job_description(
            db=db_mock,
            recruiter=recruiter,
            job=job,
        )


def test_service_does_not_mutate_or_persist_job():
    recruiter_id = uuid4()
    job_id = uuid4()

    recruiter = Recruiter(
        id=recruiter_id,
        user_id=uuid4(),
    )

    original_description = "Original unmutated description text."
    job = Job(
        id=job_id,
        recruiter_id=recruiter_id,
        title="Python Dev",
        description=original_description,
        employment_type="Full-time",
    )
    job.job_skills = []

    service = JobDescriptionAnalyzerService()
    mock_gemini = MagicMock()
    mock_gemini.generate_structured.return_value = make_mock_ai_result()
    service.gemini_service = mock_gemini

    db_mock = MagicMock()

    service.analyze_job_description(
        db=db_mock,
        recruiter=recruiter,
        job=job,
    )

    # Verify db.commit() was NOT called
    db_mock.commit.assert_not_called()
    db_mock.add.assert_not_called()

    # Verify job object is unchanged
    assert job.description == original_description
    assert job.title == "Python Dev"
