from uuid import uuid4
import pytest

from app.ai.matching.ranking import CandidateMatch, candidate_ranker
from pydantic import ValidationError


def test_rank_candidates_by_overall_score():
    candidate_a = uuid4()
    candidate_b = uuid4()
    candidate_c = uuid4()

    candidates = [
        CandidateMatch(candidate_id=candidate_a, overall_score=0.70),
        CandidateMatch(candidate_id=candidate_b, overall_score=0.95),
        CandidateMatch(candidate_id=candidate_c, overall_score=0.82),
    ]

    results = candidate_ranker.rank(candidates)

    assert results[0].candidate_id == candidate_b
    assert results[0].overall_score == 0.95
    assert results[0].rank == 1

    assert results[1].candidate_id == candidate_c
    assert results[1].overall_score == 0.82
    assert results[1].rank == 2

    assert results[2].candidate_id == candidate_a
    assert results[2].overall_score == 0.70
    assert results[2].rank == 3

def test_rank_candidates_with_equal_scores():
    candidate_a = uuid4()
    candidate_b = uuid4()
    candidate_c = uuid4()

    candidates = [
        CandidateMatch(candidate_id=candidate_a, overall_score=0.91),
        CandidateMatch(candidate_id=candidate_b, overall_score=0.91),
        CandidateMatch(candidate_id=candidate_c, overall_score=0.85),
    ]

    results = candidate_ranker.rank(candidates)

    assert results[0].candidate_id == candidate_a
    assert results[0].overall_score == 0.91
    assert results[0].rank == 1

    assert results[1].candidate_id == candidate_b
    assert results[1].overall_score == 0.91
    assert results[1].rank == 2

    assert results[2].candidate_id == candidate_c
    assert results[2].overall_score == 0.85
    assert results[2].rank == 3

def test_rank_candidates_with_empty_input():
    results = candidate_ranker.rank([])

    assert results == []

def test_candidate_match_rejects_invalid_score():
    candidate_id = uuid4()

    with pytest.raises(ValidationError):
        CandidateMatch(
            candidate_id=candidate_id,
            overall_score=1.1,
        )

    with pytest.raises(ValidationError):
        CandidateMatch(
            candidate_id=candidate_id,
            overall_score=-0.1,
        )