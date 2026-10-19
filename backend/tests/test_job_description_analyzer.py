from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.ai.job_description_analyzer.context import (
    JobDescriptionContext,
    JobDescriptionContextBuilder,
)
from app.ai.job_description_analyzer.prompts import (
    JobDescriptionPromptBuilder,
)
from app.ai.job_description_analyzer.schemas import (
    IssueCategory,
    IssuePriority,
    JobDescriptionAIResult,
    JobDescriptionAnalysisResponse,
    JobDescriptionAnalysisResult,
    JobDescriptionIssue,
    JobSkillsAnalysis,
)
from app.models.job import Job


# =====================================================================
# Schema Tests
# =====================================================================

def test_job_description_issue_valid():
    issue = JobDescriptionIssue(
        priority=IssuePriority.HIGH,
        category=IssueCategory.REQUIREMENTS,
        title="Unclear years of experience",
        explanation="The job mentions 'senior' but does not specify required years or scope.",
        suggested_action="Specify minimum 5+ years of experience with distributed systems.",
    )
    assert issue.priority == IssuePriority.HIGH
    assert issue.category == IssueCategory.REQUIREMENTS
    assert "Unclear" in issue.title


def test_job_description_issue_rejects_invalid_enums():
    with pytest.raises(ValidationError):
        JobDescriptionIssue(
            priority="critical",  # invalid priority
            category=IssueCategory.CLARITY,
            title="Bad priority",
            explanation="Test",
            suggested_action="Fix",
        )

    with pytest.raises(ValidationError):
        JobDescriptionIssue(
            priority=IssuePriority.MEDIUM,
            category="invalid_category",  # invalid category
            title="Bad category",
            explanation="Test",
            suggested_action="Fix",
        )


def test_job_description_ai_result_quality_score_bounds():
    valid_data = {
        "quality_score": 85,
        "overall_assessment": "Solid description with clear scope.",
        "strengths": ["Well-defined tech stack."],
        "issues": [],
        "missing_information": ["Remote policy."],
        "skills_analysis": {
            "required_skills_evaluation": "Good coverage of Python.",
            "preferred_skills_evaluation": "Nice to have Redis.",
            "unmentioned_skills_in_description": [],
            "suggested_skills_to_add": [],
        },
        "improvement_recommendations": ["Add day-to-day bullets."],
        "improved_description": "Cleaned up draft.",
    }

    result = JobDescriptionAIResult.model_validate(valid_data)
    assert result.quality_score == 85

    # Test score < 0
    with pytest.raises(ValidationError):
        JobDescriptionAIResult.model_validate({**valid_data, "quality_score": -1})

    # Test score > 100
    with pytest.raises(ValidationError):
        JobDescriptionAIResult.model_validate({**valid_data, "quality_score": 105})


def test_job_description_response_schema():
    job_id = uuid4()
    skills_analysis = JobSkillsAnalysis(
        required_skills_evaluation="Python and FastAPI are clearly required.",
        preferred_skills_evaluation="Docker is listed as nice to have.",
        unmentioned_skills_in_description=["PostgreSQL"],
        suggested_skills_to_add=["Kubernetes"],
    )
    result = JobDescriptionAnalysisResult(
        quality_score=78,
        overall_assessment="Well-structured but missing team context.",
        strengths=["Clear responsibilities."],
        issues=[
            JobDescriptionIssue(
                priority=IssuePriority.MEDIUM,
                category=IssueCategory.CLARITY,
                title="Vague team reporting structure",
                explanation="Does not state who this role reports to.",
                suggested_action="Specify engineering manager or tech lead.",
            )
        ],
        missing_information=["Team size and manager."],
        skills_analysis=skills_analysis,
        improvement_recommendations=["Add team context."],
        improved_description="Revised job description with [Placeholders].",
    )
    response = JobDescriptionAnalysisResponse(
        job_id=job_id,
        analysis=result,
    )
    assert response.job_id == job_id
    assert response.analysis.quality_score == 78
    assert "heuristic evaluation" in response.analysis.disclaimer


# =====================================================================
# Context Builder Tests
# =====================================================================

def test_context_builder_valid():
    job_id = uuid4()
    recruiter_id = uuid4()
    job = Job(
        id=job_id,
        recruiter_id=recruiter_id,
        title="Senior Backend Engineer",
        description="Design and implement scalable Python APIs and microservices.",
        location="Bengaluru",
        employment_type="Full-time",
        experience_level="Senior",
        salary_min=1500000,
        salary_max=2500000,
        is_active=True,
    )

    builder = JobDescriptionContextBuilder()
    context = builder.build(
        job=job,
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker", "AWS"],
    )

    assert context.job_id == job_id
    assert context.title == "Senior Backend Engineer"
    assert context.description == "Design and implement scalable Python APIs and microservices."
    assert context.location == "Bengaluru"
    assert context.salary_min == 1500000
    assert context.salary_max == 2500000
    assert context.required_skills == ["FastAPI", "Python"]
    assert context.preferred_skills == ["AWS", "Docker"]


def test_context_builder_normalizes_and_deduplicates_skills():
    job = Job(
        id=uuid4(),
        recruiter_id=uuid4(),
        title="Backend Dev",
        description="Write code.",
        employment_type="Full-time",
    )

    builder = JobDescriptionContextBuilder()
    context = builder.build(
        job=job,
        required_skills=[" Python ", "fastapi", "Python", ""],
        preferred_skills=["  Docker  ", "docker", "AWS"],
    )

    assert context.required_skills == ["Python", "fastapi"]
    assert context.preferred_skills == ["AWS", "Docker"]


def test_context_builder_rejects_empty_description():
    job = Job(
        id=uuid4(),
        recruiter_id=uuid4(),
        title="Empty Job",
        description="   ",
        employment_type="Full-time",
    )

    builder = JobDescriptionContextBuilder()
    with pytest.raises(ValueError, match="Job description cannot be empty"):
        builder.build(job=job)


def test_context_builder_handles_none_optional_fields():
    job = Job(
        id=uuid4(),
        recruiter_id=uuid4(),
        title="Minimal Job",
        description="Valid description with minimal metadata.",
        employment_type="Contract",
        location=None,
        experience_level=None,
        salary_min=None,
        salary_max=None,
    )

    builder = JobDescriptionContextBuilder()
    context = builder.build(job=job)

    assert context.location is None
    assert context.experience_level is None
    assert context.salary_min is None
    assert context.salary_max is None
    assert context.required_skills == []
    assert context.preferred_skills == []


# =====================================================================
# Prompt Builder Tests
# =====================================================================

def test_prompt_builder_includes_grounding_and_anti_injection():
    context = JobDescriptionContext(
        job_id=uuid4(),
        title="Staff AI Engineer",
        description="Build LLM inference pipelines with sub-100ms latency.",
        location="Remote",
        employment_type="Full-time",
        experience_level="Staff",
        salary_min=3000000,
        salary_max=4500000,
        required_skills=["PyTorch", "Python"],
        preferred_skills=["Triton"],
    )

    builder = JobDescriptionPromptBuilder()
    prompt = builder.build(context=context)

    # Core grounding constraints
    assert "ANTI-FABRICATION" in prompt
    assert "NEVER invent salary" in prompt
    assert "NEVER invent or alter work location" in prompt

    # Prompt injection defenses
    assert "PROMPT INJECTION DEFENSE" in prompt
    assert "UNTRUSTED USER INPUT" in prompt

    # Explicit placeholder instructions
    assert "placeholders" in prompt.lower()

    # Job context presence
    assert "Staff AI Engineer" in prompt
    assert "Build LLM inference pipelines" in prompt
    assert "PyTorch, Python" in prompt
    assert "Triton" in prompt
