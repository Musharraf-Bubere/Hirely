from app.ai.matching.ranking import (
    CandidateMatch,
    RankedCandidate,
    candidate_ranker,
)
from app.ai.matching.results import CompleteMatchResult
from app.ai.matching.scoring import MatchScoreResult


class MatchingService:
    def to_candidate_match(
        self,
        result: MatchScoreResult,
    ) -> CandidateMatch:
        return CandidateMatch(
            candidate_id=result.candidate_id,
            overall_score=result.overall_score,
        )

    def rank_matches(
        self,
        results: list[MatchScoreResult],
    ) -> list[RankedCandidate]:
        candidate_matches = [
            self.to_candidate_match(result)
            for result in results
        ]

        return candidate_ranker.rank(candidate_matches)

    def rank_complete_matches(
        self,
        results: list[CompleteMatchResult],
    ) -> list[RankedCandidate]:
        score_results = [
            result.score
            for result in results
        ]

        return self.rank_matches(score_results)


matching_service = MatchingService()