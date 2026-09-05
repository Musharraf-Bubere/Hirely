from uuid import uuid4

import pytest

from app.ai.matching.engine import MatchingEngine
from app.ai.matching.scoring import MatchingConfig
from app.ai.matching.skill_matching import SkillMatcher


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

    assert result.score.candidate_id == candidate_id
    assert result.score.required_skill_score == 0.5
    assert result.score.preferred_skill_score == 0.0
    assert result.score.semantic_similarity == 1.0
    assert result.score.overall_score == 0.55

    assert result.skills.required_matched == ["Python"]
    assert result.skills.required_missing == ["FastAPI"]
    assert result.skills.preferred_matched == []
    assert result.skills.preferred_missing == ["Docker"]


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

    assert result.score.candidate_id == candidate_id
    assert result.score.required_skill_score == 1.0
    assert result.score.preferred_skill_score == 1.0
    assert result.score.semantic_similarity == 1.0
    assert result.score.overall_score == 1.0

    assert result.skills.required_matched == ["Python"]
    assert result.skills.required_missing == []
    assert result.skills.preferred_matched == []
    assert result.skills.preferred_missing == []


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

    assert result.score.candidate_id == candidate_id
    assert result.score.required_skill_score == 1.0
    assert result.score.preferred_skill_score is None
    assert result.score.semantic_similarity == 1.0
    assert result.score.overall_score == 1.0

    assert result.skills.required_matched == ["Python"]
    assert result.skills.required_missing == []
    assert result.skills.preferred_matched == []
    assert result.skills.preferred_missing == []


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

    assert result.score.candidate_id == candidate_id
    assert result.score.semantic_similarity == 0.0
    assert result.score.required_skill_score == 1.0
    assert result.score.preferred_skill_score == 1.0

    assert result.skills.required_matched == ["Python"]
    assert result.skills.required_missing == []
    assert result.skills.preferred_matched == []
    assert result.skills.preferred_missing == []