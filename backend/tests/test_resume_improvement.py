from uuid import UUID, uuid4
import pytest
from pydantic import ValidationError

from app.ai.ats_analyzer.analyzer import ATSDeterministicResult
from app.ai.ats_analyzer.schemas import ATSScoreBreakdown
from app.ai.parsers.schemas import (
    Certification,
    Education,
    Project,
    ResumeData,
    WorkExperience,
)
from app.ai.resume_improvement.analyzer import (
    ResumeImprovementAnalyzer,
    ResumeImprovementDeterministicResult,
)
from app.ai.resume_improvement.context import (
    ResumeImprovementCandidateContext,
    ResumeImprovementContext,
    ResumeImprovementContextBuilder,
    ResumeImprovementDeterministicSignalsContext,
    ResumeImprovementJobContext,
    resume_improvement_context_builder,
)
from app.ai.resume_improvement.prompts import (
    ResumeImprovementPromptBuilder,
    resume_improvement_prompt_builder,
)
from app.ai.resume_improvement.schemas import (
    ActionPriority,
    ImprovementAction,
    ResumeImprovementAIResult,
    ResumeImprovementRequest,
    ResumeImprovementResponse,
    ResumeImprovementResult,
    SectionImprovement,
    SectionStatus,
)


# =====================================================================
# Fixtures and Helpers
# =====================================================================

def make_sample_resume_data(
    *,
    skills: list[str] | None = None,
    with_contact_pii: bool = True,
    complete: bool = True,
) -> ResumeData:
    if not complete:
        return ResumeData()

    return ResumeData(
        name="Alex Smith",
        email="alex.smith@secret-personal.com" if with_contact_pii else None,
        phone="+1 (555) 987-6543" if with_contact_pii else None,
        location="San Francisco, CA, USA",
        headline="Senior Backend Engineer",
        summary="Experienced backend engineer building distributed systems with Python and PostgreSQL.",
        skills=skills or ["Python", "PostgreSQL", "Docker"],
        experience=[
            WorkExperience(
                company="TechCorp Inc.",
                job_title="Senior Backend Engineer",
                start_date="2022-01",
                end_date="2025-06",
                description="Designed and deployed microservices handling 10k requests per minute.",
            )
        ],
        projects=[
            Project(
                name="Hirely Platform",
                description="AI-driven recruitment intelligence engine.",
                technologies=["Python", "FastAPI", "PostgreSQL"],
            )
        ],
        education=[
            Education(
                institution="State University",
                degree="B.S.",
                field_of_study="Computer Science",
                start_date="2016",
                end_date="2020",
            )
        ],
        certifications=[
            Certification(
                name="AWS Certified Solutions Architect",
                issuer="Amazon Web Services",
                date="2023",
            )
        ],
    )


def make_sample_deterministic_signals(
    *,
    ats_score: int = 80,
    required_matched: list[str] | None = None,
    required_missing: list[str] | None = None,
    preferred_matched: list[str] | None = None,
    preferred_missing: list[str] | None = None,
    empty_sections: list[str] | None = None,
) -> ResumeImprovementDeterministicSignalsContext:
    return ResumeImprovementDeterministicSignalsContext(
        ats_score=ats_score,
        required_skill_score=0.8,
        preferred_skill_score=0.5,
        semantic_relevance_score=0.75,
        resume_completeness_score=0.9,
        required_skills_matched=required_matched or ["Python", "FastAPI"],
        required_skills_missing=required_missing or ["Redis"],
        preferred_skills_matched=preferred_matched or ["Docker"],
        preferred_skills_missing=preferred_missing or ["Kubernetes"],
        empty_or_missing_sections=empty_sections or [],
    )


# =====================================================================
# A. Pydantic Schemas Tests
# =====================================================================

def test_request_schema_with_valid_uuid():
    job_id = uuid4()
    req = ResumeImprovementRequest(job_id=job_id)
    assert req.job_id == job_id
    assert isinstance(req.job_id, UUID)


def test_request_schema_rejects_missing_or_invalid_job_id():
    with pytest.raises(ValidationError):
        ResumeImprovementRequest()  # missing job_id

    with pytest.raises(ValidationError):
        ResumeImprovementRequest(job_id="not-a-valid-uuid")


def test_improvement_action_valid():
    action = ImprovementAction(
        priority=ActionPriority.HIGH,
        category="Skills",
        title="Add Redis Experience If Applicable",
        recommendation="If you used Redis for caching in Hirely, specify your caching strategy.",
        rationale="Target role lists Redis as a mandatory requirement.",
        requires_candidate_verification=True,
    )
    assert action.priority == ActionPriority.HIGH
    assert action.priority.value == "high"
    assert action.requires_candidate_verification is True
    assert action.category == "Skills"


def test_improvement_action_accepts_valid_string_enums():
    action = ImprovementAction(
        priority="medium",
        category="Summary",
        title="Align Summary with Cloud Architecture",
        recommendation="Mention distributed systems experience earlier in the summary.",
        rationale="Job description focuses heavily on cloud architectures.",
        requires_candidate_verification=False,
    )
    assert action.priority == ActionPriority.MEDIUM
    assert action.priority == "medium"
    assert action.requires_candidate_verification is False


def test_improvement_action_rejects_invalid_priority():
    with pytest.raises(ValidationError):
        ImprovementAction(
            priority="critical",  # invalid priority enum
            category="Skills",
            title="Invalid",
            recommendation="Test",
            rationale="Test",
        )


def test_section_improvement_valid():
    sec = SectionImprovement(
        section_name="Work Experience",
        current_status=SectionStatus.NEEDS_IMPROVEMENT,
        suggestions=["Add specific system metrics if verified."],
    )
    assert sec.section_name == "Work Experience"
    assert sec.current_status == SectionStatus.NEEDS_IMPROVEMENT
    assert len(sec.suggestions) == 1


def test_section_improvement_rejects_invalid_status():
    with pytest.raises(ValidationError):
        SectionImprovement(
            section_name="Projects",
            current_status="mediocre",  # invalid section status
            suggestions=[],
        )


def test_resume_improvement_ai_result_valid():
    ai_result = ResumeImprovementAIResult(
        overall_assessment="Strong background in Python with minor qualification gaps in caching.",
        prioritized_actions=[
            ImprovementAction(
                priority="high",
                category="Skills",
                title="Address Redis Requirement",
                recommendation="If experienced with Redis, mention key operations.",
                rationale="Redis is required.",
                requires_candidate_verification=True,
            )
        ],
        required_skill_recommendations=["Highlight Redis experience if applicable."],
        preferred_skill_recommendations=["Highlight Kubernetes deployment experience."],
        section_improvements=[
            SectionImprovement(
                section_name="Summary",
                current_status="strong",
                suggestions=["Tailor first sentence to backend systems."],
            )
        ],
        summary_improvements=["Mention backend scaling."],
        experience_improvements=["Detail microservice communication."],
        project_improvements=["Explain system architecture in Hirely project."],
        skills_improvements=["Standardize PostgreSQL terminology."],
    )

    json_str = ai_result.model_dump_json()
    assert "overall_assessment" in json_str
    assert "prioritized_actions" in json_str
    assert "requires_candidate_verification" in json_str


def test_resume_improvement_result_score_constraints():
    breakdown = ATSScoreBreakdown(
        required_skill_score=0.8,
        preferred_skill_score=0.5,
        semantic_relevance_score=0.7,
        resume_completeness_score=0.9,
    )

    # Valid score in [0, 100]
    result = ResumeImprovementResult(
        overall_assessment="Good alignment",
        ats_score=85,
        score_breakdown=breakdown,
    )
    assert result.ats_score == 85

    # Out of range: score > 100
    with pytest.raises(ValidationError):
        ResumeImprovementResult(
            overall_assessment="Good alignment",
            ats_score=105,
            score_breakdown=breakdown,
        )

    # Out of range: score < 0
    with pytest.raises(ValidationError):
        ResumeImprovementResult(
            overall_assessment="Good alignment",
            ats_score=-1,
            score_breakdown=breakdown,
        )


def test_resume_improvement_response_valid():
    job_id = uuid4()
    breakdown = ATSScoreBreakdown(
        required_skill_score=0.9,
        preferred_skill_score=0.6,
        semantic_relevance_score=0.8,
        resume_completeness_score=1.0,
    )
    result = ResumeImprovementResult(
        overall_assessment="Solid match for the role.",
        ats_score=88,
        score_breakdown=breakdown,
        missing_required_skills=["Redis"],
        missing_preferred_skills=["Kubernetes"],
    )
    response = ResumeImprovementResponse(
        job_id=job_id,
        resume_improvement=result,
    )
    assert response.job_id == job_id
    assert response.resume_improvement.ats_score == 88
    assert response.resume_improvement.missing_required_skills == ["Redis"]


# =====================================================================
# B. Context Builder & Privacy / PII Sanitization Tests
# =====================================================================

def test_context_builder_combines_and_normalizes_skills():
    builder = ResumeImprovementContextBuilder()
    resume_data = make_sample_resume_data(skills=[" Python ", "FastAPI", "docker "])
    candidate_skills = ["python", "SQLAlchemy", "FastAPI"]
    signals = make_sample_deterministic_signals()

    context = builder.build(
        first_name="Jane",
        last_name="Doe",
        headline="Fullstack",
        bio="Dev",
        location="India",
        candidate_skills=candidate_skills,
        resume_data=resume_data,
        job_title="Backend Engineer",
        job_description="Python/FastAPI role",
        job_location="Remote",
        employment_type="Full-time",
        experience_level="Mid",
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker"],
        deterministic_signals=signals,
    )

    skills = context.candidate.skills
    # Should be deduplicated, stripped, and sorted
    assert "FastAPI" in skills
    assert "SQLAlchemy" in skills
    assert "docker" in skills
    assert "Python" in skills
    assert len(skills) == len(set(skills))


def test_context_builder_excludes_email_and_phone():
    builder = ResumeImprovementContextBuilder()
    resume_data = make_sample_resume_data(with_contact_pii=True)
    signals = make_sample_deterministic_signals()

    context = builder.build(
        first_name="Alex",
        last_name="Smith",
        headline="Engineer",
        bio="Bio text",
        location="San Francisco, CA",
        candidate_skills=["Python"],
        resume_data=resume_data,
        job_title="Backend Developer",
        job_description="Job description",
        job_location="San Francisco",
        employment_type="Full-time",
        experience_level="Senior",
        required_skills=["Python"],
        preferred_skills=[],
        deterministic_signals=signals,
    )

    # 1. Inspect object attributes: candidate context must not have email or phone attributes
    assert not hasattr(context.candidate, "email")
    assert not hasattr(context.candidate, "phone")

    # 2. Test actual serialization boundary: serialized JSON payload must not contain PII
    serialized_context = context.model_dump_json()
    assert "alex.smith@secret-personal.com" not in serialized_context
    assert "+1 (555) 987-6543" not in serialized_context
    assert "987-6543" not in serialized_context


def test_context_builder_excludes_internal_ids_and_file_paths():
    builder = ResumeImprovementContextBuilder()
    resume_data = make_sample_resume_data()
    signals = make_sample_deterministic_signals()

    context = builder.build(
        first_name="Alex",
        last_name="Smith",
        headline="Engineer",
        bio="Bio",
        location="City",
        candidate_skills=["Python"],
        resume_data=resume_data,
        job_title="Engineer",
        job_description="Desc",
        job_location="Remote",
        employment_type="Full-time",
        experience_level="Mid",
        required_skills=["Python"],
        preferred_skills=[],
        deterministic_signals=signals,
    )

    serialized = context.model_dump_json()
    # Confirm internal identifiers or storage paths are never leaked
    assert "user_id" not in serialized
    assert "candidate_id" not in serialized
    assert "resume_id" not in serialized
    assert "file_path" not in serialized
    assert "original_filename" not in serialized


def test_context_builder_handles_empty_optional_sections():
    builder = ResumeImprovementContextBuilder()
    empty_resume = make_sample_resume_data(complete=False)
    signals = make_sample_deterministic_signals(empty_sections=["All"])

    context = builder.build(
        first_name=None,
        last_name=None,
        headline=None,
        bio=None,
        location=None,
        candidate_skills=[],
        resume_data=empty_resume,
        job_title="Python Developer",
        job_description="Build APIs",
        job_location=None,
        employment_type=None,
        experience_level=None,
        required_skills=[],
        preferred_skills=[],
        deterministic_signals=signals,
    )

    assert context.candidate.name is None
    assert context.candidate.headline is None
    assert context.candidate.skills == []
    assert context.candidate.experience == []
    assert context.candidate.projects == []
    assert context.job.location is None


# =====================================================================
# C. Deterministic Analyzer Tests
# =====================================================================

def test_deterministic_analyzer_preserves_matched_and_missing_skills(monkeypatch):
    analyzer = ResumeImprovementAnalyzer()

    # Mock semantic analyzer embedding call
    monkeypatch.setattr(
        analyzer.ats_semantic_analyzer,
        "calculate",
        lambda ats_context: 0.70,
    )

    candidate = type(
        "Candidate",
        (),
        {
            "first_name": "Dev",
            "last_name": "User",
            "headline": "Backend Engineer",
            "bio": "Dev bio",
            "location": "Bengaluru",
        },
    )()

    job = type(
        "Job",
        (),
        {
            "title": "Backend Engineer",
            "description": "API developer role",
            "location": "Bengaluru",
            "employment_type": "Full-time",
            "experience_level": "Mid",
        },
    )()

    resume = make_sample_resume_data(skills=["Python", "PostgreSQL", "Docker"])

    result = analyzer.analyze(
        candidate=candidate,
        candidate_skills=["Python"],
        resume_data=resume,
        job=job,
        required_skills=["Python", "FastAPI", "PostgreSQL"],
        preferred_skills=["Docker", "Kubernetes"],
    )

    assert isinstance(result, ResumeImprovementDeterministicResult)
    # Python & PostgreSQL matched, FastAPI missing
    assert set(result.deterministic_result.required_skills_matched) == {
        "Python",
        "PostgreSQL",
    }
    assert result.deterministic_result.required_skills_missing == ["FastAPI"]

    # Preferred skills Docker & Kubernetes
    # Sample resume has Docker, so Docker matched, Kubernetes missing
    assert "Docker" in result.deterministic_result.preferred_skills_matched
    assert "Kubernetes" in result.deterministic_result.preferred_skills_missing


def test_deterministic_analyzer_detects_empty_sections():
    analyzer = ResumeImprovementAnalyzer()

    empty_resume = ResumeData(
        name="Empty Candidate",
        skills=[],
        experience=[],
        projects=[],
        education=[],
        certifications=[],
        summary=None,
    )

    empty_sections = analyzer._detect_empty_or_missing_sections(empty_resume)
    assert "Professional Summary" in empty_sections
    assert "Work Experience" in empty_sections
    assert "Projects" in empty_sections
    assert "Skills" in empty_sections
    assert "Education" in empty_sections
    assert "Certifications" in empty_sections

    complete_resume = make_sample_resume_data(complete=True)
    complete_empty_sections = analyzer._detect_empty_or_missing_sections(complete_resume)
    assert complete_empty_sections == []


def test_deterministic_analyzer_score_formula_weights(monkeypatch):
    analyzer = ResumeImprovementAnalyzer()

    # Deterministic signals
    req_score = 0.80
    pref_score = 0.60
    sem_score = 0.70
    comp_score = 0.90

    monkeypatch.setattr(
        analyzer.ats_semantic_analyzer,
        "calculate",
        lambda ctx: sem_score,
    )

    candidate = type(
        "Candidate",
        (),
        {
            "first_name": "Test",
            "last_name": "Candidate",
            "headline": "Tester",
            "bio": "Bio",
            "location": "Remote",
        },
    )()

    job = type(
        "Job",
        (),
        {
            "title": "Developer",
            "description": "Desc",
            "location": "Remote",
            "employment_type": "Full-time",
            "experience_level": "Mid",
        },
    )()

    # Mock ATS analyzer analyze return value directly to verify scoring integration
    from app.ai.ats_analyzer.analyzer import ATSDeterministicResult

    mock_deterministic = ATSDeterministicResult(
        required_skill_score=req_score,
        preferred_skill_score=pref_score,
        resume_completeness_score=comp_score,
        required_skills_matched=["Python"],
        required_skills_missing=[],
        preferred_skills_matched=[],
        preferred_skills_missing=[],
    )

    monkeypatch.setattr(
        analyzer.ats_analyzer,
        "analyze",
        lambda ctx: mock_deterministic,
    )

    result = analyzer.analyze(
        candidate=candidate,
        candidate_skills=["Python"],
        resume_data=make_sample_resume_data(),
        job=job,
        required_skills=["Python"],
        preferred_skills=[],
    )

    expected_score = round(
        (
            req_score * 0.45
            + pref_score * 0.15
            + sem_score * 0.30
            + comp_score * 0.10
        )
        * 100
    )

    assert result.ats_score == expected_score
    assert result.score_breakdown.required_skill_score == req_score
    assert result.score_breakdown.preferred_skill_score == pref_score
    assert result.score_breakdown.semantic_relevance_score == sem_score
    assert result.score_breakdown.resume_completeness_score == comp_score


def test_deterministic_analyzer_is_deterministic(monkeypatch):
    analyzer = ResumeImprovementAnalyzer()
    monkeypatch.setattr(
        analyzer.ats_semantic_analyzer,
        "calculate",
        lambda ctx: 0.65,
    )

    candidate = type(
        "Candidate",
        (),
        {"first_name": "A", "last_name": "B", "headline": "C", "bio": "D", "location": "E"},
    )()
    job = type(
        "Job",
        (),
        {"title": "T", "description": "D", "location": "L", "employment_type": "F", "experience_level": "M"},
    )()
    resume = make_sample_resume_data()

    res1 = analyzer.analyze(
        candidate=candidate,
        candidate_skills=["Python"],
        resume_data=resume,
        job=job,
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker"],
    )

    res2 = analyzer.analyze(
        candidate=candidate,
        candidate_skills=["Python"],
        resume_data=resume,
        job=job,
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker"],
    )

    assert res1.ats_score == res2.ats_score
    assert res1.score_breakdown == res2.score_breakdown
    assert res1.empty_or_missing_sections == res2.empty_or_missing_sections


# =====================================================================
# D. Prompt Builder Tests
# =====================================================================

def test_prompt_builder_contains_target_job_and_candidate_evidence():
    builder = ResumeImprovementPromptBuilder()
    resume_data = make_sample_resume_data(skills=["Python", "PostgreSQL"])
    signals = make_sample_deterministic_signals(
        ats_score=78,
        required_matched=["Python"],
        required_missing=["Redis"],
    )

    context = resume_improvement_context_builder.build(
        first_name="Morgan",
        last_name="Freeman",
        headline="Principal Architect",
        bio="Building systems",
        location="Chicago, IL",
        candidate_skills=["Python"],
        resume_data=resume_data,
        job_title="Lead Distributed Systems Engineer",
        job_description="Architect distributed event-driven systems using Redis and Kafka.",
        job_location="Chicago, IL",
        employment_type="Full-time",
        experience_level="Lead",
        required_skills=["Python", "Redis"],
        preferred_skills=["Kafka"],
        deterministic_signals=signals,
    )

    prompt = builder.build(context=context)

    # Asserts context presence
    assert "Lead Distributed Systems Engineer" in prompt
    assert "Redis and Kafka" in prompt
    assert "Morgan Freeman" in prompt
    assert "Principal Architect" in prompt
    assert "Redis" in prompt


def test_prompt_builder_enforces_anti_fabrication_rules():
    builder = ResumeImprovementPromptBuilder()
    resume_data = make_sample_resume_data()
    signals = make_sample_deterministic_signals()

    context = resume_improvement_context_builder.build(
        first_name="Dev",
        last_name="Tester",
        headline="Dev",
        bio="Dev",
        location="Remote",
        candidate_skills=["Python"],
        resume_data=resume_data,
        job_title="Python Engineer",
        job_description="Build APIs",
        job_location="Remote",
        employment_type="Full-time",
        experience_level="Mid",
        required_skills=["Python"],
        preferred_skills=[],
        deterministic_signals=signals,
    )

    prompt = builder.build(context=context)

    # Anti-fabrication assertions
    assert "Never invent or fabricate" in prompt
    assert "Employers or companies" in prompt
    assert "Job titles or roles" in prompt
    assert "Employment dates or durations" in prompt
    assert "Performance metrics, percentages, revenue figures" in prompt
    assert "No keyword stuffing" in prompt or "no keyword stuffing" in prompt.lower()


def test_prompt_builder_enforces_conditional_verification_contract():
    builder = ResumeImprovementPromptBuilder()
    resume_data = make_sample_resume_data()
    signals = make_sample_deterministic_signals()

    context = resume_improvement_context_builder.build(
        first_name="Dev",
        last_name="Tester",
        headline="Dev",
        bio="Dev",
        location="Remote",
        candidate_skills=["Python"],
        resume_data=resume_data,
        job_title="Python Engineer",
        job_description="Build APIs",
        job_location="Remote",
        employment_type="Full-time",
        experience_level="Mid",
        required_skills=["Python"],
        preferred_skills=[],
        deterministic_signals=signals,
    )

    prompt = builder.build(context=context)

    # Must specify candidate verification rule and conditional advice pattern
    assert "requires_candidate_verification" in prompt
    assert "If you have hands-on experience with" in prompt
    assert "do not claim it" in prompt


def test_prompt_builder_never_includes_contact_pii_or_internal_paths():
    builder = ResumeImprovementPromptBuilder()
    # Inject sensitive contact info in the raw resume
    resume_data = make_sample_resume_data(with_contact_pii=True)
    signals = make_sample_deterministic_signals()

    context = resume_improvement_context_builder.build(
        first_name="Secret",
        last_name="Candidate",
        headline="Dev",
        bio="Dev",
        location="Hidden Street 123",
        candidate_skills=["Python"],
        resume_data=resume_data,
        job_title="Python Developer",
        job_description="Description",
        job_location="Remote",
        employment_type="Full-time",
        experience_level="Mid",
        required_skills=["Python"],
        preferred_skills=[],
        deterministic_signals=signals,
    )

    prompt = builder.build(context=context)

    # Strict check: Contact PII must NOT appear anywhere in the LLM prompt
    assert "alex.smith@secret-personal.com" not in prompt
    assert "+1 (555) 987-6543" not in prompt
    assert "candidate_id" not in prompt
    assert "resume_id" not in prompt
    assert "file_path" not in prompt
