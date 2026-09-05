from uuid import uuid4
import pytest

from app.ai.matching.engine import MatchingEngine
from app.ai.matching.scoring import MatchingConfig
from app.ai.matching.skill_matching import SkillMatcher
from app.ai.services.matching_service import matching_service


def test_matching_engine_to_ranking_pipeline():
    engine = MatchingEngine(
        skill_matcher=SkillMatcher(),
        scoring_config=MatchingConfig(),
    )

    candidate_a = uuid4()
    candidate_b = uuid4()
    candidate_c = uuid4()

    result_a = engine.match(
        candidate_id=candidate_a,
        candidate_skills=["Python", "FastAPI", "Docker"],
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker", "PostgreSQL"],
        candidate_embedding=[1.0, 0.0],
        job_embedding=[1.0, 0.0],
    )

    result_b = engine.match(
        candidate_id=candidate_b,
        candidate_skills=[
            "Python",
            "FastAPI",
            "Docker",
            "PostgreSQL",
        ],
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker", "PostgreSQL"],
        candidate_embedding=[1.0, 0.0],
        job_embedding=[1.0, 0.0],
    )

    result_c = engine.match(
        candidate_id=candidate_c,
        candidate_skills=["Python"],
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker", "PostgreSQL"],
        candidate_embedding=[1.0, 0.0],
        job_embedding=[-1.0, 0.0],
    )

    ranked = matching_service.rank_matches(
        [result_a, result_b, result_c]
    )

    assert ranked[0].candidate_id == candidate_b
    assert ranked[0].overall_score == pytest.approx(1.0)
    assert ranked[0].rank == 1

    assert ranked[1].candidate_id == candidate_a
    assert ranked[1].overall_score == pytest.approx(0.9)
    assert ranked[1].rank == 2

    assert ranked[2].candidate_id == candidate_c
    assert ranked[2].overall_score == pytest.approx(0.25)
    assert ranked[2].rank == 3