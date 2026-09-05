from app.ai.matching.ranking import (
    CandidateMatch,
    RankedCandidate,
    candidate_ranker,
)
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


matching_service = MatchingService()