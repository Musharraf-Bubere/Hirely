from uuid import UUID

from app.ai.matching.explanation import (
    MatchExplanation,
    MatchExplanationEvidence,
    MatchExplanationInput,
)
from app.ai.matching.explanation_prompt import ExplanationPromptBuilder
from app.ai.services.match_explanation_service import MatchExplanationService


class FakeGeminiService:
    def __init__(self):
        self.received_prompt = None
        self.received_schema = None

    def generate_structured(self, prompt, response_schema):
        self.received_prompt = prompt
        self.received_schema = response_schema

        return MatchExplanation(
            summary="Strong match for the role.",
            strengths=[
                "Matches all required skills.",
            ],
            gaps=[
                "Docker is missing.",
            ],
            evidence=MatchExplanationEvidence(
                required_skill_score=1.0,
                preferred_skill_score=0.5,
                semantic_similarity=0.91,
            ),
            caveats=[],
        )


def test_match_explanation_service_generates_structured_explanation():
    fake_gemini = FakeGeminiService()
    service = MatchExplanationService(
        gemini_service=fake_gemini,
        prompt_builder=ExplanationPromptBuilder(),
    )

    data = MatchExplanationInput(
        candidate_id=UUID("11111111-1111-1111-1111-111111111111"),
        overall_score=0.9,
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.91,
        required_matched=["Python", "FastAPI"],
        required_missing=["Docker"],
        preferred_matched=["AWS"],
        preferred_missing=["Kubernetes"],
    )

    result = service.explain(data)

    assert isinstance(result, MatchExplanation)
    assert result.summary == "Strong match for the role."
    assert result.evidence.required_skill_score == 1.0

    assert fake_gemini.received_schema is MatchExplanation
    assert "Python, FastAPI" in fake_gemini.received_prompt
    assert "Docker" in fake_gemini.received_prompt
    assert "0.9" in fake_gemini.received_prompt