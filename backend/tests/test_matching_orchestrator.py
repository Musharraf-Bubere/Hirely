from uuid import uuid4, UUID
import pytest

from pydantic import ValidationError

from app.ai.matching.engine import MatchingEngine
from app.ai.matching.results import CompleteMatchResult, RankedMatchResult
from app.ai.matching.scoring import MatchScoreResult
from app.ai.matching.skill_matching import SkillMatchResult
from app.ai.services.matching_orchestrator import (
    MatchingInput,
    MatchingOrchestrator,
    MultiCandidateMatchingInput,
    ExplanationRequest,
)
from app.ai.services.matching_service import MatchingService
from app.ai.services.match_explanation_service import MatchExplanationService
from app.ai.matching.explanation import MatchExplanation, MatchExplanationEvidence


class FakeMatchingEngine:
    def __init__(self, result: CompleteMatchResult):
        self.result = result
        self.received_arguments = None

    def match(
        self,
        candidate_id,
        candidate_skills,
        required_skills,
        preferred_skills,
        candidate_embedding,
        job_embedding,
    ):
        self.received_arguments = {
            "candidate_id": candidate_id,
            "candidate_skills": candidate_skills,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "candidate_embedding": candidate_embedding,
            "job_embedding": job_embedding,
        }

        return self.result

class FakeMatchExplanationService:
    def __init__(self, explanation):
        self.explanation = explanation
        self.received_data = []

    def explain(self, data):
        self.received_data.append(data)
        return self.explanation


def test_matching_orchestrator_delegates_to_matching_engine():
    candidate_id = uuid4()

    expected_result = CompleteMatchResult(
        score=MatchScoreResult(
            candidate_id=candidate_id,
            overall_score=0.85,
            required_skill_score=1.0,
            preferred_skill_score=0.5,
            semantic_similarity=0.8,
        ),
        skills=SkillMatchResult(
            required_score=1.0,
            preferred_score=0.5,
            required_matched=["Python"],
            required_missing=[],
            preferred_matched=["AWS"],
            preferred_missing=["Docker"],
        ),
    )

    fake_engine = FakeMatchingEngine(expected_result)
    orchestrator = MatchingOrchestrator(
        matching_engine=fake_engine,
        matching_service=MatchingService(),
        match_explanation_service=FakeMatchExplanationService(explanation=None),
    )

    data = MatchingInput(
        candidate_id=candidate_id,
        candidate_skills=["Python", "AWS"],
        required_skills=["Python"],
        preferred_skills=["AWS", "Docker"],
        candidate_embedding=[0.1, 0.2, 0.3],
        job_embedding=[0.2, 0.3, 0.4],
    )

    result = orchestrator.match(data)

    assert result == expected_result

    assert fake_engine.received_arguments == {
        "candidate_id": candidate_id,
        "candidate_skills": ["Python", "AWS"],
        "required_skills": ["Python"],
        "preferred_skills": ["AWS", "Docker"],
        "candidate_embedding": [0.1, 0.2, 0.3],
        "job_embedding": [0.2, 0.3, 0.4],
    }

def test_matching_orchestrator_matches_multiple_candidates():
    candidate_id_a = uuid4()
    candidate_id_b = uuid4()

    result_a = CompleteMatchResult(
        score=MatchScoreResult(
            candidate_id=candidate_id_a,
            overall_score=0.90,
            required_skill_score=1.0,
            preferred_skill_score=0.5,
            semantic_similarity=0.8,
        ),
        skills=SkillMatchResult(
            required_score=1.0,
            preferred_score=0.5,
            required_matched=["Python"],
            required_missing=[],
            preferred_matched=["AWS"],
            preferred_missing=["Docker"],
        ),
    )

    result_b = CompleteMatchResult(
        score=MatchScoreResult(
            candidate_id=candidate_id_b,
            overall_score=0.70,
            required_skill_score=0.5,
            preferred_skill_score=0.5,
            semantic_similarity=0.6,
        ),
        skills=SkillMatchResult(
            required_score=0.5,
            preferred_score=0.5,
            required_matched=["Python"],
            required_missing=["FastAPI"],
            preferred_matched=["AWS"],
            preferred_missing=["Docker"],
        ),
    )

    fake_engine = FakeMatchingEngine(result_a)

    original_match = fake_engine.match
    results = [result_a, result_b]

    def fake_match(
        candidate_id,
        candidate_skills,
        required_skills,
        preferred_skills,
        candidate_embedding,
        job_embedding,
    ):
        fake_engine.received_arguments = {
            "candidate_id": candidate_id,
            "candidate_skills": candidate_skills,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "candidate_embedding": candidate_embedding,
            "job_embedding": job_embedding,
        }

        return results.pop(0)

    fake_engine.match = fake_match

    orchestrator = MatchingOrchestrator(
        matching_engine=fake_engine,
        matching_service=MatchingService(),
        match_explanation_service=FakeMatchExplanationService(explanation=None),
    )

    input_data = MultiCandidateMatchingInput(
        candidates=[
            MatchingInput(
                candidate_id=candidate_id_a,
                candidate_skills=["Python", "AWS"],
                required_skills=["Python"],
                preferred_skills=["AWS"],
                candidate_embedding=[0.1, 0.2, 0.3],
                job_embedding=[0.2, 0.3, 0.4],
            ),
            MatchingInput(
                candidate_id=candidate_id_b,
                candidate_skills=["Python"],
                required_skills=["Python", "FastAPI"],
                preferred_skills=["AWS"],
                candidate_embedding=[0.4, 0.5, 0.6],
                job_embedding=[0.2, 0.3, 0.4],
            ),
        ]
    )

    matched_results = orchestrator.match_candidates(input_data)

    assert matched_results == [result_a, result_b]

def test_matching_orchestrator_ranks_multiple_candidates():
    candidate_id_a = uuid4()
    candidate_id_b = uuid4()
    candidate_id_c = uuid4()

    results = [
        CompleteMatchResult(
            score=MatchScoreResult(
                candidate_id=candidate_id_a,
                overall_score=0.70,
                required_skill_score=0.6,
                preferred_skill_score=0.5,
                semantic_similarity=0.7,
            ),
            skills=SkillMatchResult(
                required_score=0.6,
                preferred_score=0.5,
                required_matched=["Python"],
                required_missing=["FastAPI"],
                preferred_matched=["AWS"],
                preferred_missing=[],
            ),
        ),
        CompleteMatchResult(
            score=MatchScoreResult(
                candidate_id=candidate_id_b,
                overall_score=0.90,
                required_skill_score=1.0,
                preferred_skill_score=1.0,
                semantic_similarity=0.8,
            ),
            skills=SkillMatchResult(
                required_score=1.0,
                preferred_score=1.0,
                required_matched=["Python", "FastAPI"],
                required_missing=[],
                preferred_matched=["AWS"],
                preferred_missing=[],
            ),
        ),
        CompleteMatchResult(
            score=MatchScoreResult(
                candidate_id=candidate_id_c,
                overall_score=0.80,
                required_skill_score=0.8,
                preferred_skill_score=0.5,
                semantic_similarity=0.8,
            ),
            skills=SkillMatchResult(
                required_score=0.8,
                preferred_score=0.5,
                required_matched=["Python"],
                required_missing=["FastAPI"],
                preferred_matched=["AWS"],
                preferred_missing=[],
            ),
        ),
    ]

    fake_engine = FakeMatchingEngine(results[0])
    results_to_return = results.copy()

    def fake_match(
        candidate_id,
        candidate_skills,
        required_skills,
        preferred_skills,
        candidate_embedding,
        job_embedding,
    ):
        return results_to_return.pop(0)

    fake_engine.match = fake_match

    orchestrator = MatchingOrchestrator(
        matching_engine=fake_engine,
        matching_service=MatchingService(),
        match_explanation_service=FakeMatchExplanationService(explanation=None),
    )

    input_data = MultiCandidateMatchingInput(
        candidates=[
            MatchingInput(
                candidate_id=candidate_id_a,
                candidate_skills=["Python"],
                required_skills=["Python", "FastAPI"],
                preferred_skills=["AWS"],
                candidate_embedding=[0.1, 0.2, 0.3],
                job_embedding=[0.2, 0.3, 0.4],
            ),
            MatchingInput(
                candidate_id=candidate_id_b,
                candidate_skills=["Python", "FastAPI", "AWS"],
                required_skills=["Python", "FastAPI"],
                preferred_skills=["AWS"],
                candidate_embedding=[0.4, 0.5, 0.6],
                job_embedding=[0.2, 0.3, 0.4],
            ),
            MatchingInput(
                candidate_id=candidate_id_c,
                candidate_skills=["Python", "AWS"],
                required_skills=["Python", "FastAPI"],
                preferred_skills=["AWS"],
                candidate_embedding=[0.7, 0.8, 0.9],
                job_embedding=[0.2, 0.3, 0.4],
            ),
        ]
    )

    ranked_candidates = orchestrator.rank_candidates(input_data)

    assert [candidate.candidate_id for candidate in ranked_candidates] == [
        candidate_id_b,
        candidate_id_c,
        candidate_id_a,
    ]

    assert [candidate.overall_score for candidate in ranked_candidates] == [
        0.90,
        0.80,
        0.70,
    ]

def test_matching_orchestrator_returns_ranked_match_results():
    candidate_id_a = uuid4()
    candidate_id_b = uuid4()

    result_a = CompleteMatchResult(
        score=MatchScoreResult(
            candidate_id=candidate_id_a,
            overall_score=0.70,
            required_skill_score=0.5,
            preferred_skill_score=0.5,
            semantic_similarity=0.7,
        ),
        skills=SkillMatchResult(
            required_score=0.5,
            preferred_score=0.5,
            required_matched=["Python"],
            required_missing=["FastAPI"],
            preferred_matched=["AWS"],
            preferred_missing=["Docker"],
        ),
    )

    result_b = CompleteMatchResult(
        score=MatchScoreResult(
            candidate_id=candidate_id_b,
            overall_score=0.90,
            required_skill_score=1.0,
            preferred_skill_score=1.0,
            semantic_similarity=0.8,
        ),
        skills=SkillMatchResult(
            required_score=1.0,
            preferred_score=1.0,
            required_matched=["Python", "FastAPI"],
            required_missing=[],
            preferred_matched=["AWS"],
            preferred_missing=[],
        ),
    )

    fake_engine = FakeMatchingEngine(result_a)
    results_to_return = [result_a, result_b]

    def fake_match(
        candidate_id,
        candidate_skills,
        required_skills,
        preferred_skills,
        candidate_embedding,
        job_embedding,
    ):
        return results_to_return.pop(0)

    fake_engine.match = fake_match

    orchestrator = MatchingOrchestrator(
        matching_engine=fake_engine,
        matching_service=MatchingService(),
        match_explanation_service=FakeMatchExplanationService(explanation=None),
    )

    input_data = MultiCandidateMatchingInput(
        candidates=[
            MatchingInput(
                candidate_id=candidate_id_a,
                candidate_skills=["Python"],
                required_skills=["Python", "FastAPI"],
                preferred_skills=["AWS", "Docker"],
                candidate_embedding=[0.1, 0.2, 0.3],
                job_embedding=[0.2, 0.3, 0.4],
            ),
            MatchingInput(
                candidate_id=candidate_id_b,
                candidate_skills=["Python", "FastAPI", "AWS"],
                required_skills=["Python", "FastAPI"],
                preferred_skills=["AWS"],
                candidate_embedding=[0.4, 0.5, 0.6],
                job_embedding=[0.2, 0.3, 0.4],
            ),
        ]
    )

    ranked_results = orchestrator.rank_match_results(input_data)

    assert len(ranked_results) == 2

    assert ranked_results[0].rank == 1
    assert ranked_results[0].candidate_id == candidate_id_b
    assert ranked_results[0].overall_score == 0.90
    assert ranked_results[0].required_skill_score == 1.0
    assert ranked_results[0].preferred_skill_score == 1.0
    assert ranked_results[0].semantic_similarity == 0.8
    assert ranked_results[0].required_matched == ["Python", "FastAPI"]
    assert ranked_results[0].required_missing == []
    assert ranked_results[0].preferred_matched == ["AWS"]
    assert ranked_results[0].preferred_missing == []

    assert ranked_results[1].rank == 2
    assert ranked_results[1].candidate_id == candidate_id_a
    assert ranked_results[1].overall_score == 0.70
    assert ranked_results[1].required_matched == ["Python"]
    assert ranked_results[1].required_missing == ["FastAPI"]

def test_matching_orchestrator_explains_ranked_match():
    candidate_id = uuid4()

    ranked_match = RankedMatchResult(
        rank=1,
        candidate_id=candidate_id,
        overall_score=0.90,
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.8,
        required_matched=["Python", "FastAPI"],
        required_missing=[],
        preferred_matched=["AWS"],
        preferred_missing=["Docker"],
    )

    expected_explanation = MatchExplanation(
        summary="Strong match based on the provided evidence.",
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

    fake_explanation_service = FakeMatchExplanationService(
        explanation=expected_explanation
    )

    orchestrator = MatchingOrchestrator(
        matching_engine=FakeMatchingEngine(
            result=CompleteMatchResult(
                score=MatchScoreResult(
                    candidate_id=candidate_id,
                    overall_score=0.90,
                    required_skill_score=1.0,
                    preferred_skill_score=0.5,
                    semantic_similarity=0.8,
                ),
                skills=SkillMatchResult(
                    required_score=1.0,
                    preferred_score=0.5,
                    required_matched=["Python", "FastAPI"],
                    required_missing=[],
                    preferred_matched=["AWS"],
                    preferred_missing=["Docker"],
                ),
            )
        ),
        matching_service=MatchingService(),
        match_explanation_service=fake_explanation_service,
    )

    result = orchestrator.explain_match(ranked_match)

    assert result.match == ranked_match
    assert result.explanation == expected_explanation

    assert len(fake_explanation_service.received_data) == 1

    explanation_input = fake_explanation_service.received_data[0]

    assert explanation_input.candidate_id == candidate_id
    assert explanation_input.overall_score == 0.90
    assert explanation_input.required_skill_score == 1.0
    assert explanation_input.preferred_skill_score == 0.5
    assert explanation_input.semantic_similarity == 0.8
    assert explanation_input.required_matched == ["Python", "FastAPI"]
    assert explanation_input.required_missing == []
    assert explanation_input.preferred_matched == ["AWS"]
    assert explanation_input.preferred_missing == ["Docker"]

def test_matching_orchestrator_explains_only_top_n_ranked_matches():
    candidate_1 = UUID("11111111-1111-1111-1111-111111111111")
    candidate_2 = UUID("22222222-2222-2222-2222-222222222222")
    candidate_3 = UUID("33333333-3333-3333-3333-333333333333")

    ranked_matches = [
        RankedMatchResult(
            rank=1,
            candidate_id=candidate_1,
            overall_score=0.95,
            required_skill_score=0.9,
            preferred_skill_score=0.8,
            semantic_similarity=0.95,
            required_matched=["Python"],
            required_missing=[],
            preferred_matched=["AWS"],
            preferred_missing=[],
        ),
        RankedMatchResult(
            rank=2,
            candidate_id=candidate_2,
            overall_score=0.85,
            required_skill_score=0.8,
            preferred_skill_score=0.7,
            semantic_similarity=0.85,
            required_matched=["Python"],
            required_missing=["Docker"],
            preferred_matched=[],
            preferred_missing=["AWS"],
        ),
        RankedMatchResult(
            rank=3,
            candidate_id=candidate_3,
            overall_score=0.75,
            required_skill_score=0.7,
            preferred_skill_score=0.6,
            semantic_similarity=0.75,
            required_matched=["Python"],
            required_missing=["Docker"],
            preferred_matched=[],
            preferred_missing=["AWS"],
        ),
    ]

    explanation = MatchExplanation(
        summary="Strong candidate match.",
        strengths=["Python"],
        gaps=[],
        evidence=MatchExplanationEvidence(
            required_skill_score=0.9,
            preferred_skill_score=0.8,
            semantic_similarity=0.95,
        ),
        caveats=[],
    )

    fake_explanation_service = FakeMatchExplanationService(
        explanation=explanation
    )

    orchestrator = MatchingOrchestrator(
        matching_engine=FakeMatchingEngine(None),
        matching_service=MatchingService(),
        match_explanation_service=fake_explanation_service,
    )

    request = ExplanationRequest(
        ranked_matches=ranked_matches,
        explanation_limit=2,
    )

    results = orchestrator.explain_ranked_matches(request)

    assert len(results) == 3
    assert results[0].match.candidate_id == candidate_1
    assert results[1].match.candidate_id == candidate_2
    assert results[2].match.candidate_id == candidate_3

    assert results[0].explanation == explanation
    assert results[1].explanation == explanation
    assert results[2].explanation is None

    assert len(fake_explanation_service.received_data) == 2
    assert {
        data.candidate_id
        for data in fake_explanation_service.received_data
    } == {candidate_1, candidate_2}

def test_matching_orchestrator_explains_all_when_limit_exceeds_candidates():
    candidate_1 = UUID("11111111-1111-1111-1111-111111111111")
    candidate_2 = UUID("22222222-2222-2222-2222-222222222222")

    ranked_matches = [
        RankedMatchResult(
            rank=1,
            candidate_id=candidate_1,
            overall_score=0.95,
            required_skill_score=0.9,
            preferred_skill_score=0.8,
            semantic_similarity=0.95,
            required_matched=["Python"],
            required_missing=[],
            preferred_matched=["AWS"],
            preferred_missing=[],
        ),
        RankedMatchResult(
            rank=2,
            candidate_id=candidate_2,
            overall_score=0.85,
            required_skill_score=0.8,
            preferred_skill_score=0.7,
            semantic_similarity=0.85,
            required_matched=["Python"],
            required_missing=["Docker"],
            preferred_matched=[],
            preferred_missing=["AWS"],
        ),
    ]

    explanation = MatchExplanation(
        summary="Strong candidate match.",
        strengths=["Python"],
        gaps=[],
        evidence=MatchExplanationEvidence(
            required_skill_score=0.9,
            preferred_skill_score=0.8,
            semantic_similarity=0.95,
        ),
        caveats=[],
    )

    fake_explanation_service = FakeMatchExplanationService(
        explanation=explanation
    )

    orchestrator = MatchingOrchestrator(
        matching_engine=FakeMatchingEngine(None),
        matching_service=MatchingService(),
        match_explanation_service=fake_explanation_service,
    )

    request = ExplanationRequest(
        ranked_matches=ranked_matches,
        explanation_limit=5,
    )

    results = orchestrator.explain_ranked_matches(request)

    assert len(results) == 2
    assert results[0].explanation == explanation
    assert results[1].explanation == explanation
    assert len(fake_explanation_service.received_data) == 2

def test_explanation_request_rejects_invalid_explanation_limit():
    with pytest.raises(ValidationError):
        ExplanationRequest(
            ranked_matches=[],
            explanation_limit=0,
        )

    with pytest.raises(ValidationError):
        ExplanationRequest(
            ranked_matches=[],
            explanation_limit=-1,
        )


def test_matching_orchestrator_explains_ranked_matches_in_order():
    candidate_1 = UUID("11111111-1111-1111-1111-111111111111")
    candidate_2 = UUID("22222222-2222-2222-2222-222222222222")

    ranked_matches = [
        RankedMatchResult(
            rank=1,
            candidate_id=candidate_1,
            overall_score=0.95,
            required_skill_score=0.9,
            preferred_skill_score=0.8,
            semantic_similarity=0.95,
            required_matched=["Python"],
            required_missing=[],
            preferred_matched=["AWS"],
            preferred_missing=[],
        ),
        RankedMatchResult(
            rank=2,
            candidate_id=candidate_2,
            overall_score=0.85,
            required_skill_score=0.8,
            preferred_skill_score=0.7,
            semantic_similarity=0.85,
            required_matched=["FastAPI"],
            required_missing=["Docker"],
            preferred_matched=[],
            preferred_missing=["AWS"],
        ),
    ]

    explanation = MatchExplanation(
        summary="Candidate matches the job requirements.",
        strengths=["Relevant skills"],
        gaps=["Docker"],
        evidence=MatchExplanationEvidence(
            required_skill_score=0.9,
            preferred_skill_score=0.8,
            semantic_similarity=0.95,
        ),
        caveats=[],
    )

    fake_explanation_service = FakeMatchExplanationService(
        explanation=explanation
    )

    orchestrator = MatchingOrchestrator(
        matching_engine=FakeMatchingEngine(None),
        matching_service=MatchingService(),
        match_explanation_service=fake_explanation_service,
    )

    request = ExplanationRequest(
        ranked_matches=ranked_matches,
        explanation_limit=2,
    )

    results = orchestrator.explain_ranked_matches(request)

    received_candidate_ids = [
        data.candidate_id
        for data in fake_explanation_service.received_data
    ]

    assert received_candidate_ids == [
        candidate_1,
        candidate_2,
    ]

    assert [
        result.match.candidate_id
        for result in results
    ] == [
        candidate_1,
        candidate_2,
    ]