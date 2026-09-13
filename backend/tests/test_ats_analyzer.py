from app.ai.ats_analyzer.analyzer import ATSAnalyzer
from app.ai.ats_analyzer.context import (
    ATSCandidateContext,
    ATSContext,
    ATSJobContext,
)
from app.ai.ats_analyzer.schemas import ATSScoreBreakdown
from app.ai.parsers.schemas import (
    Education,
    Project,
    ResumeData,
    WorkExperience,
)


def build_resume(
    *,
    skills: list[str] | None = None,
    complete: bool = True,
) -> ResumeData:
    if not complete:
        return ResumeData()

    return ResumeData(
        name="John Doe",
        email="john@example.com",
        phone="1234567890",
        location="Mumbai",
        headline="Python Developer",
        summary="Backend developer with Python experience.",
        skills=skills or ["Python", "FastAPI"],
        experience=[
            WorkExperience(
                company="Example Corp",
                job_title="Python Developer",
                start_date="2024",
                end_date="2026",
                description="Built backend APIs.",
            )
        ],
        projects=[
            Project(
                name="Hirely",
                description="Recruitment platform",
                technologies=["Python", "FastAPI"],
            )
        ],
        education=[
            Education(
                institution="Example University",
                degree="B.Com.",
                field_of_study="Commerce",
                start_date="2018",
                end_date="2021",
            )
        ],
    )


def build_context(
    *,
    candidate_skills: list[str] | None = None,
    resume: ResumeData | None = None,
    required_skills: list[str] | None = None,
    preferred_skills: list[str] | None = None,
) -> ATSContext:
    return ATSContext(
        candidate=ATSCandidateContext(
            name="John Doe",
            headline="Python Developer",
            bio="Backend developer.",
            location="Mumbai",
            skills=candidate_skills or [],
            resume=resume or build_resume(),
        ),
        job=ATSJobContext(
            title="Python Backend Developer",
            description="Build backend APIs using Python and FastAPI.",
            location="Mumbai",
            employment_type="Full-time",
            experience_level="Mid-level",
            required_skills=required_skills or [],
            preferred_skills=preferred_skills or [],
        ),
    )


def test_required_skills_are_matched():
    analyzer = ATSAnalyzer()

    resume = build_resume(
        skills=["Python", "FastAPI"],
    )

    context = build_context(
        candidate_skills=["Python"],
        resume=resume,
        required_skills=["Python", "FastAPI"],
    )

    result = analyzer.analyze(context)

    assert result.required_skill_score == 1.0
    assert set(result.required_skills_matched) == {
        "Python",
        "FastAPI",
    }
    assert result.required_skills_missing == []


def test_missing_required_skills_are_detected():
    analyzer = ATSAnalyzer()

    resume = build_resume(
        skills=["Python"],
    )

    context = build_context(
        candidate_skills=["Python"],
        resume=resume,
        required_skills=["Python", "FastAPI", "PostgreSQL"],
    )

    result = analyzer.analyze(context)

    assert result.required_skill_score == 1 / 3
    assert result.required_skills_matched == ["Python"]
    assert set(result.required_skills_missing) == {
        "FastAPI",
        "PostgreSQL",
    }


def test_preferred_skills_are_analyzed_separately():
    analyzer = ATSAnalyzer()

    resume = build_resume(
        skills=["Python"],
    )

    context = build_context(
        candidate_skills=["Python"],
        resume=resume,
        preferred_skills=["FastAPI", "Docker"],
    )

    result = analyzer.analyze(context)

    assert result.preferred_skill_score == 0.0
    assert result.preferred_skills_matched == []
    assert set(result.preferred_skills_missing) == {
        "FastAPI",
        "Docker",
    }


def test_resume_skills_are_combined_with_candidate_profile_skills():
    analyzer = ATSAnalyzer()

    resume = build_resume(
        skills=["FastAPI"],
    )

    context = build_context(
        candidate_skills=["Python"],
        resume=resume,
        required_skills=["Python", "FastAPI"],
    )

    result = analyzer.analyze(context)

    assert result.required_skill_score == 1.0
    assert set(result.required_skills_matched) == {
        "Python",
        "FastAPI",
    }


def test_resume_completeness_score_for_complete_resume():
    analyzer = ATSAnalyzer()

    context = build_context(
        resume=build_resume(),
    )

    result = analyzer.analyze(context)

    assert result.resume_completeness_score == 1.0


def test_resume_completeness_score_for_empty_resume():
    analyzer = ATSAnalyzer()

    context = build_context(
        resume=build_resume(complete=False),
    )

    result = analyzer.analyze(context)

    assert result.resume_completeness_score == 0.0


def test_resume_completeness_score_for_partial_resume():
    analyzer = ATSAnalyzer()

    resume = ResumeData(
        name="John Doe",
        skills=["Python"],
        education=[
            Education(
                institution="Example University",
                degree="B.Com.",
            )
        ],
    )

    context = build_context(
        resume=resume,
    )

    result = analyzer.analyze(context)

    assert result.resume_completeness_score == 3 / 10


def test_ats_score_calculation():
    from app.ai.ats_analyzer.service import ATSAnalyzerService

    service = ATSAnalyzerService()

    score = service._calculate_ats_score(
        required_skill_score=1.0,
        preferred_skill_score=1.0,
        semantic_relevance_score=1.0,
        resume_completeness_score=1.0,
    )

    assert score == 100


def test_ats_score_calculation_with_zero_signals():
    from app.ai.ats_analyzer.service import ATSAnalyzerService

    service = ATSAnalyzerService()

    score = service._calculate_ats_score(
        required_skill_score=0.0,
        preferred_skill_score=0.0,
        semantic_relevance_score=0.0,
        resume_completeness_score=0.0,
    )

    assert score == 0


def test_score_breakdown_accepts_valid_scores():
    breakdown = ATSScoreBreakdown(
        required_skill_score=0.8,
        preferred_skill_score=0.6,
        semantic_relevance_score=0.7,
        resume_completeness_score=0.9,
    )

    assert breakdown.required_skill_score == 0.8
    assert breakdown.preferred_skill_score == 0.6
    assert breakdown.semantic_relevance_score == 0.7
    assert breakdown.resume_completeness_score == 0.9