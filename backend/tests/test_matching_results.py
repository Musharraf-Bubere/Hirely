from uuid import UUID

from app.ai.matching.results import CompleteMatchResult
from app.ai.matching.scoring import MatchScoreResult
from app.ai.matching.skill_matching import SkillMatchResult


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