from pydantic import BaseModel


class MatchSignals(BaseModel):
    required_skill_score: float
    preferred_skill_score: float | None
    semantic_similarity: float


class MatchingConfig(BaseModel):
    required_skill_weight: float = 0.5
    preferred_skill_weight: float = 0.2
    semantic_weight: float = 0.3


class MatchScoreResult(BaseModel):
    overall_score: float
    required_skill_score: float
    preferred_skill_score: float | None
    semantic_similarity: float


def normalize_semantic_similarity(similarity: float) -> float:
    return (similarity + 1.0) / 2.0

def calculate_match_score(
    signals: MatchSignals,
    config: MatchingConfig,
) -> MatchScoreResult:
    weighted_score = 0.0
    available_weight = 0.0

    if signals.required_skill_score is not None:
        weighted_score += (
            signals.required_skill_score * config.required_skill_weight
        )
        available_weight += config.required_skill_weight

    if signals.preferred_skill_score is not None:
        weighted_score += (
            signals.preferred_skill_score * config.preferred_skill_weight
        )
        available_weight += config.preferred_skill_weight

    if signals.semantic_similarity is not None:
        weighted_score += (
            signals.semantic_similarity * config.semantic_weight
        )
        available_weight += config.semantic_weight

    overall_score = (
        weighted_score / available_weight
        if available_weight > 0
        else 0.0
    )

    return MatchScoreResult(
        overall_score=overall_score,
        required_skill_score=signals.required_skill_score,
        preferred_skill_score=signals.preferred_skill_score,
        semantic_similarity=signals.semantic_similarity,
    )