from pydantic import BaseModel, Field

from app.ai.matching.engine import MatchingEngine
from app.ai.matching.inputs import MatchingInput
from app.ai.matching.ranking import RankedCandidate
from app.ai.matching.results import (
    CompleteMatchResult,
    FinalMatchResult,
    RankedMatchResult,
)
from app.ai.services.match_explanation_service import MatchExplanationService
from app.ai.services.matching_service import MatchingService
from app.ai.matching.explanation import MatchExplanationInput


class MatchingOrchestrator:
    def __init__(
        self,
        matching_engine: MatchingEngine,
        matching_service: MatchingService,
        match_explanation_service: MatchExplanationService,
    ):
        self.matching_engine = matching_engine
        self.matching_service = matching_service
        self.match_explanation_service = match_explanation_service

    def match(
        self,
        data: MatchingInput,
    ) -> CompleteMatchResult:
        return self.matching_engine.match(
            candidate_id=data.candidate_id,
            candidate_skills=data.candidate_skills,
            required_skills=data.required_skills,
            preferred_skills=data.preferred_skills,
            candidate_embedding=data.candidate_embedding,
            job_embedding=data.job_embedding,
        )

    def match_candidates(
        self,
        data: MultiCandidateMatchingInput,
    ) -> list[CompleteMatchResult]:
        return [
            self.match(candidate)
            for candidate in data.candidates
        ]

    def rank_candidates(
        self,
        data: MultiCandidateMatchingInput,
    ) -> list[RankedCandidate]:
        match_results = self.match_candidates(data)

        return self.matching_service.rank_complete_matches(
            match_results
        )

    def rank_match_results(
        self,
        data: MultiCandidateMatchingInput | list[CompleteMatchResult],
    ) -> list[RankedMatchResult]:

        if isinstance(data, MultiCandidateMatchingInput):
            match_results = self.match_candidates(data)
        else:
            match_results = data

        ranked_candidates = self.matching_service.rank_complete_matches(
            match_results
        )

        match_results_by_candidate = {
            result.score.candidate_id: result
            for result in match_results
        }

        return [
            RankedMatchResult(
                rank=ranked_candidate.rank,
                candidate_id=ranked_candidate.candidate_id,
                overall_score=ranked_candidate.overall_score,
                required_skill_score=match_results_by_candidate[
                    ranked_candidate.candidate_id
                ].score.required_skill_score,
                preferred_skill_score=match_results_by_candidate[
                    ranked_candidate.candidate_id
                ].score.preferred_skill_score,
                semantic_similarity=match_results_by_candidate[
                    ranked_candidate.candidate_id
                ].score.semantic_similarity,
                required_matched=match_results_by_candidate[
                    ranked_candidate.candidate_id
                ].skills.required_matched,
                required_missing=match_results_by_candidate[
                    ranked_candidate.candidate_id
                ].skills.required_missing,
                preferred_matched=match_results_by_candidate[
                    ranked_candidate.candidate_id
                ].skills.preferred_matched,
                preferred_missing=match_results_by_candidate[
                    ranked_candidate.candidate_id
                ].skills.preferred_missing,
            )
            for ranked_candidate in ranked_candidates
        ]

    def explain_match(
        self,
        match: RankedMatchResult,
    ) -> FinalMatchResult:
        explanation_input = MatchExplanationInput(
            candidate_id=match.candidate_id,
            overall_score=match.overall_score,
            required_skill_score=match.required_skill_score,
            preferred_skill_score=match.preferred_skill_score,
            semantic_similarity=match.semantic_similarity,
            required_matched=match.required_matched,
            required_missing=match.required_missing,
            preferred_matched=match.preferred_matched,
            preferred_missing=match.preferred_missing,
        )

        explanation = self.match_explanation_service.explain(
            explanation_input
        )

        return FinalMatchResult(
            match=match,
            explanation=explanation,
        )

    def explain_ranked_matches(
        self,
        data: ExplanationRequest,
    ) -> list[FinalMatchResult]:
        selected_matches = data.ranked_matches[
            :data.explanation_limit
        ]

        selected_candidate_ids = {
            match.candidate_id
            for match in selected_matches
        }

        results: list[FinalMatchResult] = []

        for match in data.ranked_matches:
            if match.candidate_id in selected_candidate_ids:
                results.append(
                    self.explain_match(match)
                )
            else:
                results.append(
                    FinalMatchResult(
                        match=match,
                        explanation=None,
                    )
                )

        return results


class MultiCandidateMatchingInput(BaseModel):
    candidates: list[MatchingInput]


class ExplanationRequest(BaseModel):
    ranked_matches: list[RankedMatchResult]
    explanation_limit: int = Field(ge=1)