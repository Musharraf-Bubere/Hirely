from uuid import UUID

from pydantic import BaseModel, Field


class CandidateMatch(BaseModel):
    candidate_id: UUID
    overall_score: float = Field(ge=0.0, le=1.0)


class RankedCandidate(BaseModel):
    rank: int
    candidate_id: UUID
    overall_score: float

class CandidateRanker:
    def rank(
        self,
        candidates: list[CandidateMatch],
    ) -> list[RankedCandidate]:
        sorted_candidates = sorted(
            candidates,
            key=lambda candidate: candidate.overall_score,
            reverse=True,
        )

        return [
            RankedCandidate(
                rank=index,
                candidate_id=candidate.candidate_id,
                overall_score=candidate.overall_score,
            )
            for index, candidate in enumerate(sorted_candidates, start=1)
        ]


candidate_ranker = CandidateRanker()