from __future__ import annotations

from collections import defaultdict, deque
import math
import threading
from typing import Any

from app.core.observability.schemas import (
    AIErrorCategory,
    AIFeature,
    AIOperationStatus,
    estimate_token_cost,
)

# Maximum rolling latency samples per (feature, operation) pair to guarantee bounded memory.
MAX_LATENCY_SAMPLES = 1000


class AIMetricsCollector:
    """
    Thread-safe, bounded in-memory metrics collector for Hirely's AI operations.

    IMPORTANT ARCHITECTURAL CONSTRAINTS:
    1. Process-local: Metrics are maintained in-memory for the current process lifetime
       and reset on process restart.
    2. Bounded Storage: Latency samples are capped at a fixed rolling window (1,000 samples)
       to guarantee bounded memory usage.
    3. Low Cardinality: Label dimensions are strictly controlled enums (feature, operation,
       status, error_category). Dynamic IDs (candidate_id, recruiter_id, job_id, email)
       are strictly forbidden to prevent memory leaks and telemetry cardinality explosions.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._requests_total: dict[tuple[str, str, str], int] = defaultdict(int)
        self._errors_total: dict[tuple[str, str, str], int] = defaultdict(int)
        self._retries_total: dict[str, int] = defaultdict(int)
        self._fallbacks_total: dict[str, int] = defaultdict(int)
        self._rate_limit_rejections_total: int = 0
        self._tokens_total: dict[tuple[str, str], int] = defaultdict(int)
        self._estimated_cost_usd_total: dict[str, float] = defaultdict(float)
        self._rag_citations_total: dict[str, int] = defaultdict(int)
        self._rag_chunks_retrieved_total: int = 0
        self._latencies: dict[tuple[str, str], deque[float]] = defaultdict(
            lambda: deque(maxlen=MAX_LATENCY_SAMPLES)
        )

    def record_operation(
        self,
        *,
        feature: str,
        operation: str,
        status: AIOperationStatus | str,
        duration_ms: float,
        error_category: AIErrorCategory | str | None = None,
        model: str | None = None,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        total_tokens: int | None = None,
    ) -> None:
        """
        Record a completed AI operation with duration, outcome, and optional token usage.
        """
        status_val = status.value if isinstance(status, AIOperationStatus) else str(status)
        feature_val = feature.value if isinstance(feature, AIFeature) else str(feature)

        with self._lock:
            # 1. Increment request counter
            self._requests_total[(feature_val, operation, status_val)] += 1

            # 2. Record bounded latency sample
            if duration_ms >= 0:
                self._latencies[(feature_val, operation)].append(duration_ms)

            # 3. Record error if applicable
            if status_val == AIOperationStatus.ERROR.value and error_category:
                cat_val = (
                    error_category.value
                    if isinstance(error_category, AIErrorCategory)
                    else str(error_category)
                )
                self._errors_total[(feature_val, operation, cat_val)] += 1

            # 4. Record token usage and estimated cost if available
            if isinstance(prompt_tokens, int) and prompt_tokens >= 0:
                self._tokens_total[(feature_val, "prompt")] += prompt_tokens
            if isinstance(completion_tokens, int) and completion_tokens >= 0:
                self._tokens_total[(feature_val, "completion")] += completion_tokens
            if isinstance(total_tokens, int) and total_tokens >= 0:
                self._tokens_total[(feature_val, "total")] += total_tokens

            if model and isinstance(prompt_tokens, int) and prompt_tokens >= 0:
                cost = estimate_token_cost(model, prompt_tokens, completion_tokens)
                if cost:
                    self._estimated_cost_usd_total[feature_val] += cost

    def record_retry(self, *, feature: str = AIFeature.GEMINI_CLIENT.value) -> None:
        with self._lock:
            self._retries_total[str(feature)] += 1

    def record_fallback(self, *, feature: str = AIFeature.GEMINI_CLIENT.value) -> None:
        with self._lock:
            self._fallbacks_total[str(feature)] += 1

    def record_rate_limit_rejection(self) -> None:
        with self._lock:
            self._rate_limit_rejections_total += 1

    def record_rag_citations(self, *, valid_count: int, invalid_count: int) -> None:
        with self._lock:
            if valid_count > 0:
                self._rag_citations_total["valid"] += valid_count
            if invalid_count > 0:
                self._rag_citations_total["invalid"] += invalid_count

    def record_rag_chunks_retrieved(self, count: int) -> None:
        with self._lock:
            if count > 0:
                self._rag_chunks_retrieved_total += count

    @staticmethod
    def _calculate_percentile(sorted_samples: list[float], percentile: float) -> float | None:
        if not sorted_samples:
            return None
        k = (len(sorted_samples) - 1) * percentile
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return round(sorted_samples[int(k)], 2)
        d0 = sorted_samples[int(f)] * (c - k)
        d1 = sorted_samples[int(c)] * (k - f)
        return round(d0 + d1, 2)

    def get_snapshot(self) -> dict[str, Any]:
        """
        Return a thread-safe dictionary snapshot of the current in-memory metrics.
        Used for tests, health diagnostics, and administrative monitoring.
        """
        with self._lock:
            # Flatten request counters
            requests = [
                {
                    "feature": feat,
                    "operation": op,
                    "status": st,
                    "count": count,
                }
                for (feat, op, st), count in self._requests_total.items()
            ]

            # Flatten error counters
            errors = [
                {
                    "feature": feat,
                    "operation": op,
                    "error_category": cat,
                    "count": count,
                }
                for (feat, op, cat), count in self._errors_total.items()
            ]

            # Compute latency summaries
            latencies = {}
            for (feat, op), samples in self._latencies.items():
                key = f"{feat}:{op}"
                sorted_samples = sorted(samples)
                latencies[key] = {
                    "count": len(sorted_samples),
                    "min_ms": round(sorted_samples[0], 2) if sorted_samples else None,
                    "max_ms": round(sorted_samples[-1], 2) if sorted_samples else None,
                    "p50_ms": self._calculate_percentile(sorted_samples, 0.50),
                    "p90_ms": self._calculate_percentile(sorted_samples, 0.90),
                    "p95_ms": self._calculate_percentile(sorted_samples, 0.95),
                }

            tokens = {
                f"{feat}:{token_type}": count
                for (feat, token_type), count in self._tokens_total.items()
            }

            estimated_costs = {
                feat: round(cost, 6)
                for feat, cost in self._estimated_cost_usd_total.items()
            }

            return {
                "process_local_disclaimer": "Metrics are in-memory and process-local. Resets on restart.",
                "requests_total": requests,
                "errors_total": errors,
                "retries_total": dict(self._retries_total),
                "fallbacks_total": dict(self._fallbacks_total),
                "rate_limit_rejections_total": self._rate_limit_rejections_total,
                "rag_telemetry": {
                    "citations_validated": dict(self._rag_citations_total),
                    "chunks_retrieved_total": self._rag_chunks_retrieved_total,
                },
                "tokens_total": tokens,
                "estimated_costs_usd": estimated_costs,
                "latencies_ms": latencies,
            }

    def reset(self) -> None:
        """
        Clear all stored metrics. Primarily used between unit tests.
        """
        with self._lock:
            self._requests_total.clear()
            self._errors_total.clear()
            self._retries_total.clear()
            self._fallbacks_total.clear()
            self._rate_limit_rejections_total = 0
            self._tokens_total.clear()
            self._estimated_cost_usd_total.clear()
            self._rag_citations_total.clear()
            self._rag_chunks_retrieved_total = 0
            self._latencies.clear()


ai_metrics = AIMetricsCollector()


def get_ai_metrics_snapshot() -> dict[str, Any]:
    return ai_metrics.get_snapshot()


def reset_ai_metrics() -> None:
    ai_metrics.reset()
