from __future__ import annotations

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class AIErrorCategory(str, Enum):
    """
    Controlled, low-cardinality error categories for AI operations.
    Prevents raw exception leakage and telemetry metric label explosion.
    """
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    AUTHENTICATION = "authentication"
    MODEL_UNAVAILABLE = "model_unavailable"
    UPSTREAM_SERVER_ERROR = "upstream_server_error"
    CLIENT_ERROR = "client_error"
    VALIDATION_FAILED = "validation_failed"
    CITATION_INVALID = "citation_invalid"
    INTERNAL_ERROR = "internal_error"
    UNKNOWN = "unknown"


class AIFeature(str, Enum):
    """
    Controlled, low-cardinality feature identifiers.
    """
    RAG = "rag"
    CAREER_COACH = "career_coach"
    COVER_LETTER = "cover_letter"
    ATS_ANALYZER = "ats_analyzer"
    RESUME_IMPROVEMENT = "resume_improvement"
    JOB_DESCRIPTION_ANALYZER = "job_description_analyzer"
    CANDIDATE_INTELLIGENCE = "candidate_intelligence"
    RECRUITER_MATCHING = "recruiter_matching"
    MATCH_EXPLANATION = "match_explanation"
    RESUME_PARSER = "resume_parser"
    EMBEDDING = "embedding"
    RATE_LIMITER = "rate_limiter"
    GEMINI_CLIENT = "gemini_client"
    HTTP_REQUEST = "http_request"


class AIOperationStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    RETRY = "retry"
    FALLBACK = "fallback"


class AITokenUsage(BaseModel):
    """
    Captured token usage from SDK usage metadata.
    Token counts are None when not reported by the upstream API.
    Costs are strictly marked as approximate and only estimated for verified models.
    """
    prompt_tokens: int | None = Field(default=None, ge=0)
    completion_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    estimated_cost_usd: float | None = Field(default=None, ge=0.0)
    is_cost_approximate: bool = True


# Approximate pricing per 1,000,000 tokens for verified models (as of 2026 baseline)
# Format: (prompt_cost_per_1m, completion_cost_per_1m)
MODEL_PRICING_PER_1M: dict[str, tuple[float, float]] = {
    "gemini-3.5-flash-lite": (0.075, 0.30),
    "gemini-2.5-flash-lite": (0.075, 0.30),
    "gemini-1.5-flash-8b": (0.0375, 0.15),
    "gemini-3.5-flash": (0.15, 0.60),
    "gemini-2.5-flash": (0.15, 0.60),
    "gemini-1.5-flash": (0.075, 0.30),
    "gemini-embedding-2": (0.02, 0.0),
    "text-embedding-004": (0.02, 0.0),
}


def estimate_token_cost(
    model: str | None,
    prompt_tokens: int | None,
    completion_tokens: int | None,
) -> float | None:
    """
    Calculate an explicitly approximate USD cost for token consumption.
    Returns None if token counts are missing or the model has no verified pricing tier.
    """
    if not model or not isinstance(prompt_tokens, int) or prompt_tokens < 0:
        return None

    pricing = MODEL_PRICING_PER_1M.get(model)
    if not pricing:
        return None

    prompt_rate, completion_rate = pricing
    cost = (prompt_tokens / 1_000_000.0) * prompt_rate

    if isinstance(completion_tokens, int) and completion_tokens >= 0:
        cost += (completion_tokens / 1_000_000.0) * completion_rate

    return round(cost, 8)
