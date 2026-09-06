from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from app.ai.matching.results import CompleteMatchResult, RankedMatchResult, FinalMatchResult
from app.ai.matching.scoring import MatchScoreResult
from app.ai.matching.skill_matching import SkillMatchResult
from app.ai.matching.explanation import MatchExplanation


def test_complete_match_result_contains_score_and_skill_results():
    candidate_id = UUID("11111111-1111-1111-1111-111111111111")

    score_result = MatchScoreResult(
        candidate_id=candidate_id,
        overall_score=0.775,
        required_skill_score=0.75,
        preferred_skill_score=0.5,
        semantic_similarity=1.0,
    )

    skill_result = SkillMatchResult(
        required_score=0.75,
        preferred_score=0.5,
        required_matched=["Python", "FastAPI", "SQL"],
        required_missing=["Docker"],
        preferred_matched=["AWS"],
        preferred_missing=["Kubernetes"],
    )

    result = CompleteMatchResult(
        score=score_result,
        skills=skill_result,
    )

    assert result.score is score_result
    assert result.skills is skill_result
    assert result.score.candidate_id == candidate_id
    assert result.skills.required_matched == [
        "Python",
        "FastAPI",
        "SQL",
    ]

def test_ranked_match_result_accepts_valid_data():
    result = RankedMatchResult(
        rank=1,
        candidate_id=uuid4(),
        overall_score=0.90,
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.8,
        required_matched=["Python", "FastAPI"],
        required_missing=[],
        preferred_matched=["AWS"],
        preferred_missing=["Docker"],
    )

    assert result.rank == 1
    assert result.overall_score == 0.90
    assert result.required_matched == ["Python", "FastAPI"]


def test_ranked_match_result_accepts_unavailable_preferred_score():
    result = RankedMatchResult(
        rank=1,
        candidate_id=uuid4(),
        overall_score=0.85,
        required_skill_score=1.0,
        preferred_skill_score=None,
        semantic_similarity=0.7,
        required_matched=["Python"],
        required_missing=[],
        preferred_matched=[],
        preferred_missing=[],
    )

    assert result.preferred_skill_score is None


def test_ranked_match_result_rejects_invalid_score():
    with pytest.raises(ValidationError):
        RankedMatchResult(
            rank=1,
            candidate_id=uuid4(),
            overall_score=1.5,
            required_skill_score=1.0,
            preferred_skill_score=0.5,
            semantic_similarity=0.8,
            required_matched=["Python"],
            required_missing=[],
            preferred_matched=["AWS"],
            preferred_missing=[],
        )

def test_ranked_match_result_accepts_valid_data():
    result = RankedMatchResult(
        rank=1,
        candidate_id=uuid4(),
        overall_score=0.90,
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.8,
        required_matched=["Python", "FastAPI"],
        required_missing=[],
        preferred_matched=["AWS"],
        preferred_missing=["Docker"],
    )

    assert result.rank == 1
    assert result.overall_score == 0.90
    assert result.required_matched == ["Python", "FastAPI"]


def test_ranked_match_result_accepts_unavailable_preferred_score():
    result = RankedMatchResult(
        rank=1,
        candidate_id=uuid4(),
        overall_score=0.85,
        required_skill_score=1.0,
        preferred_skill_score=None,
        semantic_similarity=0.7,
        required_matched=["Python"],
        required_missing=[],
        preferred_matched=[],
        preferred_missing=[],
    )

    assert result.preferred_skill_score is None


def test_ranked_match_result_rejects_invalid_score():
    with pytest.raises(ValidationError):
        RankedMatchResult(
            rank=1,
            candidate_id=uuid4(),
            overall_score=1.5,
            required_skill_score=1.0,
            preferred_skill_score=0.5,
            semantic_similarity=0.8,
            required_matched=["Python"],
            required_missing=[],
            preferred_matched=["AWS"],
            preferred_missing=[],
        )


def test_final_match_result_accepts_match_without_explanation():
    match = RankedMatchResult(
        rank=1,
        candidate_id=uuid4(),
        overall_score=0.90,
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.8,
        required_matched=["Python", "FastAPI"],
        required_missing=[],
        preferred_matched=["AWS"],
        preferred_missing=["Docker"],
    )

    result = FinalMatchResult(match=match)

    assert result.match == match
    assert result.explanation is None


def test_final_match_result_accepts_match_with_explanation():
    match = RankedMatchResult(
        rank=1,
        candidate_id=uuid4(),
        overall_score=0.90,
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.8,
        required_matched=["Python", "FastAPI"],
        required_missing=[],
        preferred_matched=["AWS"],
        preferred_missing=["Docker"],
    )

    explanation = MatchExplanation(
        summary="Strong match based on the provided matching evidence.",
        strengths=["Python", "FastAPI"],
        gaps=["Docker"],
        evidence={
            "required_skill_score": 1.0,
            "preferred_skill_score": 0.5,
            "semantic_similarity": 0.8,
        },
        caveats=[
            "Matched skills indicate skill presence only."
        ],
    )

    result = FinalMatchResult(
        match=match,
        explanation=explanation,
    )

    assert result.match == match
    assert result.explanation == explanation