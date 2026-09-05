from uuid import uuid4

from app.ai.matching.engine import MatchingEngine
from app.ai.matching.scoring import MatchingConfig
from app.ai.matching.skill_matching import SkillMatcher
import pytest


def test_matching_engine():
    candidate_id = uuid4()

    engine = MatchingEngine(
        skill_matcher=SkillMatcher(),
        scoring_config=MatchingConfig(),
    )

    result = engine.match(
        candidate_id=candidate_id,
        candidate_skills=["Python", "SQL"],
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker"],
        candidate_embedding=[1.0, 0.0],
        job_embedding=[1.0, 0.0],
    )

    assert result.candidate_id == candidate_id
    assert result.required_skill_score == 0.5
    assert result.preferred_skill_score == 0.0
    assert result.semantic_similarity == 1.0
    assert result.overall_score == 0.55

def test_matching_engine_with_no_preferred_skills():
    candidate_id = uuid4()

    engine = MatchingEngine(
        skill_matcher=SkillMatcher(),
        scoring_config=MatchingConfig(),
    )

    result = engine.match(
        candidate_id=candidate_id,
        candidate_skills=["Python"],
        required_skills=["Python"],
        preferred_skills=[],
        candidate_embedding=[1.0, 0.0],
        job_embedding=[1.0, 0.0],
    )

    assert result.candidate_id == candidate_id
    assert result.required_skill_score == 1.0
    assert result.preferred_skill_score == 1.0
    assert result.semantic_similarity == 1.0
    assert result.overall_score == 1.0


def test_matching_engine_with_unavailable_preferred_skills():
    candidate_id = uuid4()

    engine = MatchingEngine(
        skill_matcher=SkillMatcher(),
        scoring_config=MatchingConfig(),
    )

    result = engine.match(
        candidate_id=candidate_id,
        candidate_skills=["Python"],
        required_skills=["Python"],
        preferred_skills=None,
        candidate_embedding=[1.0, 0.0],
        job_embedding=[1.0, 0.0],
    )

    assert result.candidate_id == candidate_id
    assert result.required_skill_score == 1.0
    assert result.preferred_skill_score is None
    assert result.semantic_similarity == 1.0
    assert result.overall_score == 1.0


def test_matching_engine_rejects_different_embedding_dimensions():
    candidate_id = uuid4()

    engine = MatchingEngine(
        skill_matcher=SkillMatcher(),
        scoring_config=MatchingConfig(),
    )

    with pytest.raises(ValueError, match="same dimensions"):
        engine.match(
            candidate_id=candidate_id,
            candidate_skills=["Python"],
            required_skills=["Python"],
            preferred_skills=[],
            candidate_embedding=[1.0, 0.0],
            job_embedding=[1.0, 0.0, 0.0],
        )


def test_matching_engine_rejects_empty_embedding():
    candidate_id = uuid4()

    engine = MatchingEngine(
        skill_matcher=SkillMatcher(),
        scoring_config=MatchingConfig(),
    )

    with pytest.raises(ValueError, match="cannot be empty"):
        engine.match(
            candidate_id=candidate_id,
            candidate_skills=["Python"],
            required_skills=["Python"],
            preferred_skills=[],
            candidate_embedding=[],
            job_embedding=[1.0, 0.0],
        )


def test_matching_engine_normalizes_negative_semantic_similarity():
    candidate_id = uuid4()

    engine = MatchingEngine(
        skill_matcher=SkillMatcher(),
        scoring_config=MatchingConfig(),
    )

    result = engine.match(
        candidate_id=candidate_id,
        candidate_skills=["Python"],
        required_skills=["Python"],
        preferred_skills=[],
        candidate_embedding=[1.0, 0.0],
        job_embedding=[-1.0, 0.0],
    )

    assert result.candidate_id == candidate_id
    assert result.semantic_similarity == 0.0
    assert result.required_skill_score == 1.0
    assert result.preferred_skill_score == 1.0