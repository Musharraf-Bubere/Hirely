from uuid import UUID

from app.ai.matching.skill_matching import SkillMatcher
from app.ai.matching.similarity import cosine_similarity
from app.ai.matching.scoring import (
    MatchSignals,
    MatchScoreResult,
    MatchingConfig,
    calculate_match_score,
    normalize_semantic_similarity,
)
from app.ai.matching.results import CompleteMatchResult


class MatchingEngine:
    def __init__(
        self,
        skill_matcher: SkillMatcher,
        scoring_config: MatchingConfig,
    ):
        self.skill_matcher = skill_matcher
        self.scoring_config = scoring_config

    def match(
        self,
        candidate_id: UUID,
        candidate_skills: list[str],
        required_skills: list[str],
        preferred_skills: list[str] | None,
        candidate_embedding: list[float],
        job_embedding: list[float],
    ) -> CompleteMatchResult:
        if preferred_skills is None:
            preferred_skill_score = None
            skill_result = self.skill_matcher.match(
                candidate_skills=candidate_skills,
                required_skills=required_skills,
                preferred_skills=[],
            )
        else:
            skill_result = self.skill_matcher.match(
                candidate_skills=candidate_skills,
                required_skills=required_skills,
                preferred_skills=preferred_skills,
            )
            preferred_skill_score = skill_result.preferred_score

        raw_similarity = cosine_similarity(
            candidate_embedding,
            job_embedding,
        )

        semantic_similarity = normalize_semantic_similarity(
            raw_similarity
        )

        signals = MatchSignals(
            required_skill_score=skill_result.required_score,
            preferred_skill_score=preferred_skill_score,
            semantic_similarity=semantic_similarity,
        )

        score_result = calculate_match_score(
            candidate_id=candidate_id,
            signals=signals,
            config=self.scoring_config,
        )

        return CompleteMatchResult(
            score=score_result,
            skills=skill_result,
        )


matching_engine = MatchingEngine(
    skill_matcher=SkillMatcher(),
    scoring_config=MatchingConfig(),
)