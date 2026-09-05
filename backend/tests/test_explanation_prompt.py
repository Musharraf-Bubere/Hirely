from app.ai.matching.explanation import MatchExplanationInput
from app.ai.matching.explanation_prompt import ExplanationPromptBuilder


def test_explanation_prompt_contains_matching_evidence():
    data = MatchExplanationInput(
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

    prompt = ExplanationPromptBuilder().build(data)

    assert "0.9" in prompt
    assert "1.0" in prompt
    assert "0.5" in prompt
    assert "0.91" in prompt

    assert "Python, FastAPI" in prompt
    assert "Docker" in prompt
    assert "AWS" in prompt
    assert "Kubernetes" in prompt


def test_explanation_prompt_marks_unavailable_preferred_score():
    data = MatchExplanationInput(
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

    prompt = ExplanationPromptBuilder().build(data)

    assert "Preferred Skill Score:" in prompt
    assert "Unavailable" in prompt


def test_explanation_prompt_contains_grounding_rules():
    data = MatchExplanationInput(
        candidate_id="11111111-1111-1111-1111-111111111111",
        overall_score=0.8,
        required_skill_score=0.75,
        preferred_skill_score=0.5,
        semantic_similarity=0.85,
        required_matched=["Python"],
        required_missing=["Docker"],
        preferred_matched=["AWS"],
        preferred_missing=[],
    )

    prompt = ExplanationPromptBuilder().build(data)

    assert "Do not calculate, modify, or reinterpret the overall match score." in prompt
    assert "Use only the evidence provided below." in prompt
    assert "Do not invent skills, experience, qualifications, achievements" in prompt
    assert "Do not make hiring decisions." in prompt


def test_explanation_prompt_handles_empty_skill_lists():
    data = MatchExplanationInput(
        candidate_id="11111111-1111-1111-1111-111111111111",
        overall_score=0.8,
        required_skill_score=1.0,
        preferred_skill_score=1.0,
        semantic_similarity=0.8,
        required_matched=[],
        required_missing=[],
        preferred_matched=[],
        preferred_missing=[],
    )

    prompt = ExplanationPromptBuilder().build(data)

    assert "Required Skills Matched:\nNone" in prompt
    assert "Required Skills Missing:\nNone" in prompt
    assert "Preferred Skills Matched:\nNone" in prompt
    assert "Preferred Skills Missing:\nNone" in prompt