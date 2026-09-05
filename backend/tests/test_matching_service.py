from uuid import uuid4

from app.ai.matching.scoring import MatchScoreResult
from app.ai.services.matching_service import matching_service


def test_convert_match_score_result_to_candidate_match():
    candidate_id = uuid4()

    result = MatchScoreResult(
        candidate_id=candidate_id,
        overall_score=0.91,
        required_skill_score=1.0,
        preferred_skill_score=0.5,
        semantic_similarity=0.8,
    )

    candidate_match = matching_service.to_candidate_match(result)

    assert candidate_match.candidate_id == candidate_id
    assert candidate_match.overall_score == 0.91

def test_rank_match_results():
    candidate_a = uuid4()
    candidate_b = uuid4()
    candidate_c = uuid4()

    results = [
        MatchScoreResult(
            candidate_id=candidate_a,
            overall_score=0.82,
            required_skill_score=0.8,
            preferred_skill_score=0.5,
            semantic_similarity=0.84,
        ),
        MatchScoreResult(
            candidate_id=candidate_b,
            overall_score=0.94,
            required_skill_score=1.0,
            preferred_skill_score=0.8,
            semantic_similarity=0.95,
        ),
        MatchScoreResult(
            candidate_id=candidate_c,
            overall_score=0.71,
            required_skill_score=0.6,
            preferred_skill_score=0.5,
            semantic_similarity=0.72,
        ),
    ]

    ranked = matching_service.rank_matches(results)

    assert ranked[0].candidate_id == candidate_b
    assert ranked[0].overall_score == 0.94
    assert ranked[0].rank == 1

    assert ranked[1].candidate_id == candidate_a
    assert ranked[1].overall_score == 0.82
    assert ranked[1].rank == 2

    assert ranked[2].candidate_id == candidate_c
    assert ranked[2].overall_score == 0.71
    assert ranked[2].rank == 3