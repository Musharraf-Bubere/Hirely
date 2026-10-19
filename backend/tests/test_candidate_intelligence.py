from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.ai.candidate_intelligence.schemas import (
    CandidateApplicationInfo,
    CandidateEducationItem,
    CandidateExperienceItem,
    CandidateIntelligenceFilterRequest,
    CandidateIntelligenceItem,
    CandidateIntelligenceResponse,
    CandidateProfileSummary,
)
from app.ai.matching.explanation import MatchExplanation, MatchExplanationEvidence


# =====================================================================
# Schema Tests
# =====================================================================

def test_candidate_experience_item_schema():
    exp = CandidateExperienceItem(
        job_title="Senior Python Engineer",
        company="TechCorp India",
        start_date="2022-01",
        end_date="Present",
        description="Built distributed microservices with FastAPI and Kafka.",
    )
    assert exp.job_title == "Senior Python Engineer"
    assert exp.company == "TechCorp India"


def test_candidate_education_item_schema():
    edu = CandidateEducationItem(
        degree="B.Tech",
        institution="IIT Bombay",
        field_of_study="Computer Science",
        start_date="2018",
        end_date="2022",
    )
    assert edu.degree == "B.Tech"
    assert edu.institution == "IIT Bombay"


def test_candidate_profile_summary_schema():
    candidate_id = uuid4()
    profile = CandidateProfileSummary(
        id=candidate_id,
        first_name="Jane",
        last_name="Doe",
        full_name="Jane Doe",
        headline="Staff Platform Engineer",
        location="Bengaluru",
        bio="Passionate about cloud-native systems.",
        skills=["Python", "FastAPI", "Docker", "Kubernetes"],
        experience=[
            CandidateExperienceItem(
                job_title="Platform Engineer",
                company="CloudTech",
            )
        ],
        education=[
            CandidateEducationItem(
                degree="B.E.",
                institution="Anna University",
            )
        ],
    )
    assert profile.id == candidate_id
    assert profile.full_name == "Jane Doe"
    assert len(profile.skills) == 4
    assert len(profile.experience) == 1
    assert len(profile.education) == 1


def test_candidate_intelligence_item_schema():
    candidate_id = uuid4()
    app_id = uuid4()

    item = CandidateIntelligenceItem(
        rank=1,
        candidate=CandidateProfileSummary(
            id=candidate_id,
            first_name="Jane",
            last_name="Doe",
            full_name="Jane Doe",
            skills=["Python", "FastAPI"],
        ),
        application=CandidateApplicationInfo(
            application_id=app_id,
            status="applied",
            created_at=datetime.now(timezone.utc),
        ),
        overall_score=0.88,
        required_skill_score=0.90,
        preferred_skill_score=0.75,
        semantic_similarity=0.85,
        required_matched=["Python", "FastAPI"],
        required_missing=[],
        preferred_matched=["Docker"],
        preferred_missing=["AWS"],
        explanation=MatchExplanation(
            summary="Candidate exhibits exceptional alignment with core backend requirements.",
            strengths=["Strong Python and FastAPI mastery."],
            gaps=["Missing AWS experience."],
            evidence=MatchExplanationEvidence(
                required_skill_score=0.90,
                preferred_skill_score=0.75,
                semantic_similarity=0.85,
            ),
            caveats=["AWS is nice-to-have."],
        ),
    )

    assert item.rank == 1
    assert item.overall_score == 0.88
    assert item.application.status == "applied"
    assert item.explanation is not None
    assert item.explanation.summary.startswith("Candidate exhibits")


def test_candidate_intelligence_filter_request_validation():
    # Valid filter
    req = CandidateIntelligenceFilterRequest(
        query="python",
        min_score=0.75,
        skill="FastAPI",
        application_status="applied",
        sort_by="overall_score",
        sort_order="desc",
        include_explanations=True,
        explanation_limit=5,
    )
    assert req.query == "python"
    assert req.min_score == 0.75

    # min_score < 0.0 should fail
    with pytest.raises(ValidationError):
        CandidateIntelligenceFilterRequest(min_score=-0.1)

    # min_score > 1.0 should fail
    with pytest.raises(ValidationError):
        CandidateIntelligenceFilterRequest(min_score=1.5)

    # explanation_limit < 1 should fail
    with pytest.raises(ValidationError):
        CandidateIntelligenceFilterRequest(explanation_limit=0)


def test_candidate_intelligence_response_schema():
    job_id = uuid4()
    response = CandidateIntelligenceResponse(
        job_id=job_id,
        job_title="Lead AI Engineer",
        total_candidates=10,
        matched_count=2,
        results=[],
        available_skills=["Docker", "FastAPI", "Python"],
    )
    assert response.job_id == job_id
    assert response.total_candidates == 10
    assert response.matched_count == 2
    assert "heuristic" in response.disclaimer.lower() or "deterministically" in response.disclaimer.lower()
