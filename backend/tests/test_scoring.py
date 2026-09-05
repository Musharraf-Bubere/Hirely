from uuid import uuid4
import pytest

from pydantic import ValidationError

from app.ai.matching.scoring import (
    MatchSignals,
    MatchingConfig,
    calculate_match_score,
    normalize_semantic_similarity,
    MatchScoreResult,
)


def test_calculate_match_score():
    candidate_id = uuid4()

    signals = MatchSignals(
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.8,
    )

    config = MatchingConfig()

    result = calculate_match_score(candidate_id, signals, config)

    assert result.candidate_id == candidate_id
    assert result.overall_score == 0.84
    assert result.required_skill_score == 1.0
    assert result.preferred_skill_score == 0.5
    assert result.semantic_similarity == 0.8


def test_calculate_match_score_with_custom_weights():
    candidate_id = uuid4()

    signals = MatchSignals(
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.8,
    )

    config = MatchingConfig(
        required_skill_weight=0.7,
        preferred_skill_weight=0.1,
        semantic_weight=0.2,
    )

    result = calculate_match_score(candidate_id, signals, config)

    assert result.candidate_id == candidate_id
    assert result.overall_score == 0.91


def test_calculate_match_score_ignores_unavailable_signal():
    candidate_id = uuid4()

    signals = MatchSignals(
        required_skill_score=1.0,
        preferred_skill_score=None,
        semantic_similarity=0.8,
    )

    config = MatchingConfig()

    result = calculate_match_score(candidate_id, signals, config)

    assert result.candidate_id == candidate_id
    assert result.overall_score == pytest.approx(0.925)
    assert result.required_skill_score == 1.0
    assert result.preferred_skill_score is None
    assert result.semantic_similarity == 0.8


def test_normalize_semantic_similarity():
    assert normalize_semantic_similarity(-1.0) == 0.0
    assert normalize_semantic_similarity(0.0) == 0.5
    assert normalize_semantic_similarity(1.0) == 1.0

def test_match_score_result_rejects_invalid_overall_score():
    candidate_id = uuid4()

    with pytest.raises(ValidationError):
        MatchScoreResult(
            candidate_id=candidate_id,
            overall_score=1.1,
            required_skill_score=1.0,
            preferred_skill_score=0.5,
            semantic_similarity=0.8,
        )

    with pytest.raises(ValidationError):
        MatchScoreResult(
            candidate_id=candidate_id,
            overall_score=-0.1,
            required_skill_score=1.0,
            preferred_skill_score=0.5,
            semantic_similarity=0.8,
        )