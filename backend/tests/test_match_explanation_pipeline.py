import pytest
from uuid import UUID

from app.ai.matching.engine import MatchingEngine
from app.ai.matching.explanation import MatchExplanationInput
from app.ai.matching.scoring import MatchingConfig
from app.ai.matching.skill_matching import SkillMatcher
from app.ai.services.match_explanation_service import match_explanation_service


@pytest.mark.integration
def test_match_explanation_pipeline():
    candidate_id = UUID("11111111-1111-1111-1111-111111111111")

    candidate_skills = [
        "Python",
        "FastAPI",
        "SQL",
        "AWS",
    ]

    required_skills = [
        "Python",
        "FastAPI",
        "SQL",
        "Docker",
    ]

    preferred_skills = [
        "AWS",
        "Kubernetes",
    ]

    candidate_embedding = [1.0, 0.0, 0.0]
    job_embedding = [1.0, 0.0, 0.0]

    matching_engine = MatchingEngine(
        skill_matcher=SkillMatcher(),
        scoring_config=MatchingConfig(),
    )

    match_result = matching_engine.match(
        candidate_id=candidate_id,
        candidate_skills=candidate_skills,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        candidate_embedding=candidate_embedding,
        job_embedding=job_embedding,
    )

    explanation_input = MatchExplanationInput(
        candidate_id=match_result.score.candidate_id,
        overall_score=match_result.score.overall_score,
        required_skill_score=match_result.score.required_skill_score,
        preferred_skill_score=match_result.score.preferred_skill_score,
        semantic_similarity=match_result.score.semantic_similarity,
        required_matched=match_result.skills.required_matched,
        required_missing=match_result.skills.required_missing,
        preferred_matched=match_result.skills.preferred_matched,
        preferred_missing=match_result.skills.preferred_missing,
    )

    result = match_explanation_service.explain(explanation_input)

    print(result.model_dump_json(indent=2))

    assert result.summary.strip()
    assert isinstance(result.strengths, list)
    assert isinstance(result.gaps, list)
    assert isinstance(result.caveats, list)

    assert (
        result.evidence.required_skill_score
        == match_result.score.required_skill_score
    )

    assert (
        result.evidence.preferred_skill_score
        == match_result.score.preferred_skill_score
    )

    assert (
        result.evidence.semantic_similarity
        == match_result.score.semantic_similarity
    )