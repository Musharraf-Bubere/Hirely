import pytest
from pydantic import ValidationError

from app.ai.matching.explanation import (
    MatchExplanation,
    MatchExplanationEvidence,
    MatchExplanationInput,
)


def test_match_explanation_input_accepts_valid_data():
    explanation_input = MatchExplanationInput(
        candidate_id="11111111-1111-1111-1111-111111111111",
        overall_score=0.9,
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.91,
        required_matched=["Python", "FastAPI"],
        required_missing=["Docker"],
        preferred_matched=["AWS"],
        preferred_missing=["Kubernetes"],
    )

    assert explanation_input.candidate_id is not None
    assert explanation_input.overall_score == 0.9
    assert explanation_input.required_skill_score == 1.0
    assert explanation_input.preferred_skill_score == 0.5
    assert explanation_input.semantic_similarity == 0.91


def test_match_explanation_input_accepts_unavailable_preferred_score():
    explanation_input = MatchExplanationInput(
        candidate_id="11111111-1111-1111-1111-111111111111",
        overall_score=0.95,
        required_skill_score=1.0,
        preferred_skill_score=None,
        semantic_similarity=0.9,
        required_matched=["Python"],
        required_missing=[],
        preferred_matched=[],
        preferred_missing=[],
    )

    assert explanation_input.preferred_skill_score is None


def test_match_explanation_input_rejects_invalid_score():
    with pytest.raises(ValidationError):
        MatchExplanationInput(
            candidate_id="11111111-1111-1111-1111-111111111111",
            overall_score=1.2,
            required_skill_score=1.0,
            preferred_skill_score=0.5,
            semantic_similarity=0.9,
            required_matched=["Python"],
            required_missing=[],
            preferred_matched=[],
            preferred_missing=[],
        )


def test_match_explanation_accepts_valid_data():
    explanation = MatchExplanation(
        summary="Strong match for the role.",
        strengths=[
            "Matches all required skills.",
            "Shows strong semantic alignment.",
        ],
        gaps=[
            "Docker is missing.",
        ],
        evidence=MatchExplanationEvidence(
            required_skill_score=1.0,
            preferred_skill_score=0.5,
            semantic_similarity=0.91,
        ),
        caveats=[
            "Experience duration was not evaluated.",
        ],
    )

    assert explanation.summary == "Strong match for the role."
    assert len(explanation.strengths) == 2
    assert len(explanation.gaps) == 1
    assert explanation.evidence.required_skill_score == 1.0
    assert len(explanation.caveats) == 1


def test_match_explanation_rejects_empty_summary():
    with pytest.raises(ValidationError):
        MatchExplanation(
            summary="",
            strengths=[],
            gaps=[],
            evidence=MatchExplanationEvidence(
                required_skill_score=1.0,
                preferred_skill_score=None,
                semantic_similarity=0.9,
            ),
            caveats=[],
        )