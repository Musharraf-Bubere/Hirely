from uuid import uuid4
import pytest
from pydantic import ValidationError

from app.ai.ats_analyzer.analyzer import ATSDeterministicResult
from app.ai.ats_analyzer.schemas import ATSScoreBreakdown
from app.ai.ats_analyzer.service import ats_analyzer_service
from app.ai.parsers.schemas import (
    Education,
    Project,
    ResumeData,
    WorkExperience,
)
from app.ai.resume_improvement.analyzer import (
    ResumeImprovementDeterministicResult,
)
from app.ai.resume_improvement.context import (
    ResumeImprovementContext,
    ResumeImprovementDeterministicSignalsContext,
)
from app.ai.resume_improvement.schemas import (
    ActionPriority,
    ImprovementAction,
    ResumeImprovementAIResult,
    ResumeImprovementResponse,
    SectionImprovement,
    SectionStatus,
)
from app.ai.resume_improvement.service import (
    ResumeImprovementService,
    resume_improvement_service,
)


# =====================================================================
# Fixtures and Helpers
# =====================================================================

def make_test_candidate(*, candidate_skills: list[str] | None = None):
    candidate_id = uuid4()

    candidate_skills_objects = []
    if candidate_skills:
        for skill_name in candidate_skills:
            skill_obj = type("Skill", (), {"name": skill_name})()
            cs_obj = type(
                "CandidateSkill",
                (),
                {"skill": skill_obj},
            )()
            candidate_skills_objects.append(cs_obj)

    return type(
        "Candidate",
        (),
        {
            "id": candidate_id,
            "first_name": "Jordan",
            "last_name": "Lee",
            "headline": "Full-Stack Python Engineer",
            "bio": "Experienced developer focused on backend architectures.",
            "location": "Seattle, WA",
            "candidate_skills": candidate_skills_objects,
        },
    )()


def make_test_job(
    *,
    required_skills: list[str] | None = None,
    preferred_skills: list[str] | None = None,
):
    job_id = uuid4()
    job_skills_objects = []

    for name in required_skills or []:
        skill_obj = type("Skill", (), {"name": name})()
        js_obj = type(
            "JobSkill",
            (),
            {"skill": skill_obj, "is_required": True},
        )()
        job_skills_objects.append(js_obj)

    for name in preferred_skills or []:
        skill_obj = type("Skill", (), {"name": name})()
        js_obj = type(
            "JobSkill",
            (),
            {"skill": skill_obj, "is_required": False},
        )()
        job_skills_objects.append(js_obj)

    return type(
        "Job",
        (),
        {
            "id": job_id,
            "title": "Senior Python Backend Engineer",
            "description": "Develop and maintain high-performance microservices using Python, FastAPI, and PostgreSQL.",
            "location": "Seattle, WA",
            "employment_type": "Full-time",
            "experience_level": "Senior",
            "job_skills": job_skills_objects,
        },
    )()


def make_test_resume_data():
    return ResumeData(
        name="Jordan Lee",
        email="jordan.lee@example.com",
        phone="555-0199",
        location="Seattle, WA",
        headline="Full-Stack Python Engineer",
        summary="Senior engineer with 5 years building scalable web services.",
        skills=["Python", "FastAPI", "PostgreSQL", "Docker"],
        experience=[
            WorkExperience(
                company="CloudTech",
                job_title="Software Engineer",
                start_date="2021",
                end_date="2024",
                description="Designed REST APIs using FastAPI and PostgreSQL.",
            )
        ],
        projects=[
            Project(
                name="Hirely",
                description="Recruitment intelligence system.",
                technologies=["FastAPI", "PostgreSQL"],
            )
        ],
        education=[
            Education(
                institution="Tech University",
                degree="B.S.",
                field_of_study="Computer Science",
            )
        ],
    )


def make_mock_deterministic_result():
    score_breakdown = ATSScoreBreakdown(
        required_skill_score=0.85,
        preferred_skill_score=0.60,
        semantic_relevance_score=0.80,
        resume_completeness_score=0.90,
    )

    ats_score = round(
        (0.85 * 0.45 + 0.60 * 0.15 + 0.80 * 0.30 + 0.90 * 0.10) * 100
    )

    det_result = ATSDeterministicResult(
        required_skill_score=0.85,
        preferred_skill_score=0.60,
        resume_completeness_score=0.90,
        required_skills_matched=["Python", "FastAPI"],
        required_skills_missing=["PostgreSQL"],
        preferred_skills_matched=["Docker"],
        preferred_skills_missing=["Kubernetes"],
    )

    signals_ctx = ResumeImprovementDeterministicSignalsContext(
        ats_score=ats_score,
        required_skill_score=0.85,
        preferred_skill_score=0.60,
        semantic_relevance_score=0.80,
        resume_completeness_score=0.90,
        required_skills_matched=["Python", "FastAPI"],
        required_skills_missing=["PostgreSQL"],
        preferred_skills_matched=["Docker"],
        preferred_skills_missing=["Kubernetes"],
        empty_or_missing_sections=["Certifications"],
    )

    return ResumeImprovementDeterministicResult(
        ats_score=ats_score,
        score_breakdown=score_breakdown,
        deterministic_result=det_result,
        semantic_relevance_score=0.80,
        empty_or_missing_sections=["Certifications"],
        signals_context=signals_ctx,
    )


def make_mock_ai_result():
    return ResumeImprovementAIResult(
        overall_assessment="Strong overall match for the Senior Python role with high skill alignment.",
        prioritized_actions=[
            ImprovementAction(
                priority=ActionPriority.HIGH,
                category="Skills",
                title="Highlight PostgreSQL Production Experience",
                recommendation="If you worked with PostgreSQL at CloudTech, detail indexing and queries.",
                rationale="PostgreSQL is a required core database technology for this position.",
                requires_candidate_verification=True,
            ),
            ImprovementAction(
                priority=ActionPriority.MEDIUM,
                category="Experience",
                title="Quantify API Performance",
                recommendation="Mention request volume or uptime if known from production metrics.",
                rationale="Shows senior-level impact.",
                requires_candidate_verification=False,
            ),
        ],
        required_skill_recommendations=[
            "Explicitly demonstrate PostgreSQL query design in experience."
        ],
        preferred_skill_recommendations=[
            "Highlight Kubernetes container orchestration if experienced."
        ],
        section_improvements=[
            SectionImprovement(
                section_name="Work Experience",
                current_status=SectionStatus.NEEDS_IMPROVEMENT,
                suggestions=["Add architecture and scaling details."],
            )
        ],
        summary_improvements=[
            "Align summary to emphasize microservice design."
        ],
        experience_improvements=[
            "Expand on FastAPI async endpoints."
        ],
        project_improvements=[
            "Provide context on data models in Hirely."
        ],
        skills_improvements=[
            "Group backend skills under a dedicated heading."
        ],
    )


# =====================================================================
# Service Orchestration Tests
# =====================================================================

def test_generate_improvement_orchestrates_service_workflow(monkeypatch):
    service = ResumeImprovementService()

    candidate = make_test_candidate(candidate_skills=["Python", "FastAPI"])
    job = make_test_job(
        required_skills=["Python", "FastAPI", "PostgreSQL"],
        preferred_skills=["Docker", "Kubernetes"],
    )
    resume_data = make_test_resume_data()
    deterministic_result = make_mock_deterministic_result()
    ai_result = make_mock_ai_result()

    # Mock resume retrieval
    monkeypatch.setattr(
        service,
        "_get_resume_data",
        lambda *args, **kwargs: resume_data,
    )

    # Mock deterministic analyzer
    monkeypatch.setattr(
        service.analyzer,
        "analyze",
        lambda **kwargs: deterministic_result,
    )

    # Mock prompt builder
    monkeypatch.setattr(
        service.prompt_builder,
        "build",
        lambda context: "MOCK_RESUME_IMPROVEMENT_PROMPT",
    )

    # Mock Gemini structured generation
    called_prompt = []

    def mock_generate_structured(*, prompt, response_schema):
        called_prompt.append(prompt)
        assert response_schema is ResumeImprovementAIResult
        return ai_result

    monkeypatch.setattr(
        service.gemini_service,
        "generate_structured",
        mock_generate_structured,
    )

    response = service.generate_improvement(
        db=None,
        candidate=candidate,
        job=job,
    )

    # 1. Verification of prompt invocation
    assert len(called_prompt) == 1
    assert called_prompt[0] == "MOCK_RESUME_IMPROVEMENT_PROMPT"

    # 2. Verification of response structure
    assert isinstance(response, ResumeImprovementResponse)
    assert response.job_id == job.id

    # 3. Verification of deterministic ATS preservation (NOT altered by LLM)
    assert response.resume_improvement.ats_score == deterministic_result.ats_score
    assert (
        response.resume_improvement.score_breakdown
        == deterministic_result.score_breakdown
    )
    assert response.resume_improvement.missing_required_skills == [
        "PostgreSQL"
    ]
    assert response.resume_improvement.missing_preferred_skills == [
        "Kubernetes"
    ]

    # 4. Verification of AI-generated content
    assert (
        response.resume_improvement.overall_assessment
        == ai_result.overall_assessment
    )
    assert len(response.resume_improvement.prioritized_actions) == 2
    assert (
        response.resume_improvement.prioritized_actions[0].title
        == "Highlight PostgreSQL Production Experience"
    )
    assert (
        response.resume_improvement.prioritized_actions[0].requires_candidate_verification
        is True
    )
    assert len(response.resume_improvement.section_improvements) == 1
    assert (
        response.resume_improvement.section_improvements[0].current_status
        == SectionStatus.NEEDS_IMPROVEMENT
    )


def test_generate_improvement_does_not_invoke_ats_gemini(monkeypatch):
    """
    Ensure ATS qualitative Gemini generation is NOT triggered when computing
    Resume Improvement. ATS signals should be purely deterministic and embedding-based.
    """
    service = ResumeImprovementService()

    candidate = make_test_candidate(candidate_skills=["Python"])
    job = make_test_job(required_skills=["Python"])
    resume_data = make_test_resume_data()
    deterministic_result = make_mock_deterministic_result()
    ai_result = make_mock_ai_result()

    monkeypatch.setattr(
        service,
        "_get_resume_data",
        lambda *args, **kwargs: resume_data,
    )
    monkeypatch.setattr(
        service.analyzer,
        "analyze",
        lambda **kwargs: deterministic_result,
    )

    # Spy: If ATS Gemini service is called, fail the test
    def fail_if_ats_gemini_called(*args, **kwargs):
        raise AssertionError("ATS Gemini service should NOT be invoked by Resume Improvement!")

    monkeypatch.setattr(
        ats_analyzer_service.gemini_service,
        "generate_structured",
        fail_if_ats_gemini_called,
    )

    # Mock resume improvement gemini service normally
    monkeypatch.setattr(
        service.gemini_service,
        "generate_structured",
        lambda prompt, response_schema: ai_result,
    )

    # Execute service
    response = service.generate_improvement(
        db=None,
        candidate=candidate,
        job=job,
    )
    assert response.resume_improvement.ats_score == deterministic_result.ats_score


def test_build_context_returns_context_and_deterministic_result(monkeypatch):
    service = ResumeImprovementService()

    candidate = make_test_candidate(candidate_skills=["Python"])
    job = make_test_job(required_skills=["Python"])
    resume_data = make_test_resume_data()
    deterministic_result = make_mock_deterministic_result()

    monkeypatch.setattr(
        service,
        "_get_resume_data",
        lambda *args, **kwargs: resume_data,
    )
    monkeypatch.setattr(
        service.analyzer,
        "analyze",
        lambda **kwargs: deterministic_result,
    )

    context, det_result = service.build_context(
        db=None,
        candidate=candidate,
        job=job,
    )

    assert isinstance(context, ResumeImprovementContext)
    assert isinstance(det_result, ResumeImprovementDeterministicResult)
    assert context.job.title == job.title
    assert det_result.ats_score == deterministic_result.ats_score


# =====================================================================
# Error Handling & Validation Tests
# =====================================================================

def test_missing_active_resume_raises_value_error(monkeypatch):
    service = ResumeImprovementService()
    candidate = make_test_candidate()
    job = make_test_job()

    monkeypatch.setattr(
        "app.ai.resume_improvement.service.get_active_resume",
        lambda *args, **kwargs: None,
    )

    with pytest.raises(
        ValueError,
        match="Candidate does not have an active resume.",
    ):
        service.generate_improvement(
            db=None,
            candidate=candidate,
            job=job,
        )


def test_unparsed_active_resume_raises_value_error(monkeypatch):
    service = ResumeImprovementService()
    candidate = make_test_candidate()
    job = make_test_job()

    # Case 1: Status is PENDING
    pending_resume = type(
        "Resume",
        (),
        {
            "id": uuid4(),
            "parsing_status": "PENDING",
            "parsed_data": {"name": "Test"},
        },
    )()
    monkeypatch.setattr(
        "app.ai.resume_improvement.service.get_active_resume",
        lambda *args, **kwargs: pending_resume,
    )

    with pytest.raises(
        ValueError,
        match="Candidate's active resume has not been parsed successfully.",
    ):
        service.generate_improvement(
            db=None,
            candidate=candidate,
            job=job,
        )

    # Case 2: Status is FAILED
    failed_resume = type(
        "Resume",
        (),
        {
            "id": uuid4(),
            "parsing_status": "FAILED",
            "parsed_data": None,
        },
    )()
    monkeypatch.setattr(
        "app.ai.resume_improvement.service.get_active_resume",
        lambda *args, **kwargs: failed_resume,
    )

    with pytest.raises(
        ValueError,
        match="Candidate's active resume has not been parsed successfully.",
    ):
        service.generate_improvement(
            db=None,
            candidate=candidate,
            job=job,
        )


def test_empty_parsed_data_raises_value_error(monkeypatch):
    service = ResumeImprovementService()
    candidate = make_test_candidate()
    job = make_test_job()

    empty_data_resume = type(
        "Resume",
        (),
        {
            "id": uuid4(),
            "parsing_status": "COMPLETED",
            "parsed_data": None,
        },
    )()
    monkeypatch.setattr(
        "app.ai.resume_improvement.service.get_active_resume",
        lambda *args, **kwargs: empty_data_resume,
    )

    with pytest.raises(
        ValueError,
        match="Candidate's active resume does not contain parsed data.",
    ):
        service.generate_improvement(
            db=None,
            candidate=candidate,
            job=job,
        )


def test_candidate_skills_filtering_handles_missing_or_empty_skills():
    service = ResumeImprovementService()

    # Candidate with None skill or empty skill names in association
    valid_skill = type("Skill", (), {"name": "Python"})()
    none_skill = None
    empty_skill = type("Skill", (), {"name": ""})()

    cs1 = type("CandidateSkill", (), {"skill": valid_skill})()
    cs2 = type("CandidateSkill", (), {"skill": none_skill})()
    cs3 = type("CandidateSkill", (), {"skill": empty_skill})()

    candidate = type(
        "Candidate",
        (),
        {
            "id": uuid4(),
            "candidate_skills": [cs1, cs2, cs3],
        },
    )()

    skills = service._get_candidate_skills(candidate)
    assert skills == ["Python"]


def test_job_skills_filtering_handles_missing_or_empty_skills():
    service = ResumeImprovementService()

    # Job with invalid skills in association
    valid_req = type("Skill", (), {"name": "Python"})()
    valid_pref = type("Skill", (), {"name": "Docker"})()
    none_skill = None
    empty_skill = type("Skill", (), {"name": "   "})()

    js1 = type("JobSkill", (), {"skill": valid_req, "is_required": True})()
    js2 = type("JobSkill", (), {"skill": valid_pref, "is_required": False})()
    js3 = type("JobSkill", (), {"skill": none_skill, "is_required": True})()
    js4 = type("JobSkill", (), {"skill": empty_skill, "is_required": False})()

    job = type(
        "Job",
        (),
        {
            "id": uuid4(),
            "job_skills": [js1, js2, js3, js4],
        },
    )()

    required, preferred = service._get_job_skills(job)
    assert required == ["Python"]
    assert preferred == ["Docker"]


def test_gemini_service_failure_propagates(monkeypatch):
    service = ResumeImprovementService()
    candidate = make_test_candidate()
    job = make_test_job()

    monkeypatch.setattr(
        service,
        "_get_resume_data",
        lambda *args, **kwargs: make_test_resume_data(),
    )
    monkeypatch.setattr(
        service.analyzer,
        "analyze",
        lambda **kwargs: make_mock_deterministic_result(),
    )

    def mock_failing_gemini(*args, **kwargs):
        raise RuntimeError("Gemini 503 Service Unavailable")

    monkeypatch.setattr(
        service.gemini_service,
        "generate_structured",
        mock_failing_gemini,
    )

    with pytest.raises(RuntimeError, match="Gemini 503 Service Unavailable"):
        service.generate_improvement(
            db=None,
            candidate=candidate,
            job=job,
        )


def test_deterministic_ats_values_cannot_be_overridden_by_ai(monkeypatch):
    """
    Verify that even if an AI generation attempt claims a different score or
    different missing skills, the service strictly uses the deterministic result.
    """
    service = ResumeImprovementService()
    candidate = make_test_candidate()
    job = make_test_job()

    det_result = make_mock_deterministic_result()
    det_result.ats_score = 92
    det_result.deterministic_result.required_skills_missing = ["Redis"]
    det_result.deterministic_result.preferred_skills_missing = ["Kafka"]

    monkeypatch.setattr(
        service,
        "_get_resume_data",
        lambda *args, **kwargs: make_test_resume_data(),
    )
    monkeypatch.setattr(
        service.analyzer,
        "analyze",
        lambda **kwargs: det_result,
    )

    # AI result that cannot override the numerical score
    ai_result = make_mock_ai_result()
    monkeypatch.setattr(
        service.gemini_service,
        "generate_structured",
        lambda prompt, response_schema: ai_result,
    )

    response = service.generate_improvement(
        db=None,
        candidate=candidate,
        job=job,
    )

    assert response.resume_improvement.ats_score == 92
    assert response.resume_improvement.missing_required_skills == ["Redis"]
    assert response.resume_improvement.missing_preferred_skills == ["Kafka"]
