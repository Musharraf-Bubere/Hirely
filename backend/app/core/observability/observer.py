from __future__ import annotations

import logging
import time
from types import TracebackType
from typing import Any

from app.core.observability.context import (
    feature_var,
    get_correlation_id,
    operation_var,
    pop_context_token_usage,
)
from app.core.observability.metrics import ai_metrics
from app.core.observability.sanitizer import classify_exception
from app.core.observability.schemas import (
    AIErrorCategory,
    AIFeature,
    AIOperationStatus,
    AITokenUsage,
    estimate_token_cost,
)

logger = logging.getLogger("app.ai.observability")


class AIOperationObserver:
    """
    Context manager for measuring and observing an individual AI operation.
    Guarantees fail-safe telemetry: any failure within the observability system
    is caught and silenced, ensuring business logic is never interrupted.
    """

    def __init__(
        self,
        feature: AIFeature | str,
        operation: str,
        model: str | None = None,
    ) -> None:
        self.feature = feature.value if isinstance(feature, AIFeature) else str(feature)
        self.operation = operation
        self.model = model
        self.start_time: float = 0.0
        self.duration_ms: float = 0.0

        # Token usage metadata
        self.prompt_tokens: int | None = None
        self.completion_tokens: int | None = None
        self.total_tokens: int | None = None
        self.estimated_cost_usd: float | None = None

        # Context tokens for cleanup
        self._feat_token: Any = None
        self._op_token: Any = None

        # RAG specific metadata
        self.chunk_count: int | None = None
        self.retrieval_ms: float | None = None
        self.citations_valid: bool | None = None
        self.citation_count: int | None = None

    def __enter__(self) -> "AIOperationObserver":
        self._feat_token = feature_var.set(self.feature)
        self._op_token = operation_var.set(self.operation)
        self.start_time = time.perf_counter()
        return self

    def set_model(self, model: str) -> None:
        self.model = model

    def set_token_usage(
        self,
        prompt_tokens: int | None,
        completion_tokens: int | None,
        total_tokens: int | None = None,
    ) -> None:
        """
        Record usage metadata provided by the AI SDK.
        Do not fabricate missing values.
        """
        self.prompt_tokens = prompt_tokens if isinstance(prompt_tokens, int) else None
        self.completion_tokens = completion_tokens if isinstance(completion_tokens, int) else None
        self.total_tokens = total_tokens if isinstance(total_tokens, int) else None
        if self.model and self.prompt_tokens is not None:
            self.estimated_cost_usd = estimate_token_cost(
                self.model, self.prompt_tokens, self.completion_tokens
            )

    def set_rag_metadata(
        self,
        *,
        chunk_count: int,
        retrieval_ms: float,
        citations_valid: bool,
        citation_count: int,
    ) -> None:
        self.chunk_count = chunk_count
        self.retrieval_ms = retrieval_ms
        self.citations_valid = citations_valid
        self.citation_count = citation_count

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        self.duration_ms = (time.perf_counter() - self.start_time) * 1000.0

        # Fail-safe wrapper: Telemetry failures must never break the application
        try:
            if exc_val is not None and isinstance(exc_val, Exception):
                # Classify error safely without leaking raw internals
                category, exc_class_name = classify_exception(exc_val)

                # Record error metric
                ai_metrics.record_operation(
                    feature=self.feature,
                    operation=self.operation,
                    status=AIOperationStatus.ERROR,
                    duration_ms=self.duration_ms,
                    error_category=category,
                    model=self.model,
                )

                # Emit structured error log
                logger.error(
                    "AI operation '%s:%s' failed with %s (%s) in %.2fms",
                    self.feature,
                    self.operation,
                    exc_class_name,
                    category.value,
                    self.duration_ms,
                    extra={
                        "correlation_id": get_correlation_id(),
                        "feature": self.feature,
                        "operation": self.operation,
                        "model": self.model,
                        "status": AIOperationStatus.ERROR.value,
                        "duration_ms": round(self.duration_ms, 2),
                        "error_category": category.value,
                        "exception_type": exc_class_name,
                    },
                )
            else:
                # Capture downstream token usage if not explicitly set
                if self.prompt_tokens is None:
                    ctx_tokens = pop_context_token_usage()
                    if ctx_tokens:
                        p, c, t = ctx_tokens
                        self.set_token_usage(p, c, t)

                # Record successful operation metric
                ai_metrics.record_operation(
                    feature=self.feature,
                    operation=self.operation,
                    status=AIOperationStatus.SUCCESS,
                    duration_ms=self.duration_ms,
                    model=self.model,
                    prompt_tokens=self.prompt_tokens,
                    completion_tokens=self.completion_tokens,
                    total_tokens=self.total_tokens,
                )

                extra_data: dict[str, Any] = {
                    "correlation_id": get_correlation_id(),
                    "feature": self.feature,
                    "operation": self.operation,
                    "model": self.model,
                    "status": AIOperationStatus.SUCCESS.value,
                    "duration_ms": round(self.duration_ms, 2),
                }

                if self.prompt_tokens is not None:
                    extra_data["tokens"] = {
                        "prompt": self.prompt_tokens,
                        "completion": self.completion_tokens,
                        "total": self.total_tokens,
                        "estimated_cost_usd": self.estimated_cost_usd,
                    }

                if self.chunk_count is not None:
                    extra_data["chunks_count"] = self.chunk_count
                if self.citations_valid is not None:
                    extra_data["citations_valid"] = self.citations_valid

                logger.info(
                    "AI operation '%s:%s' completed successfully in %.2fms",
                    self.feature,
                    self.operation,
                    self.duration_ms,
                    extra=extra_data,
                )

        except Exception as obs_err:
            # Silent fallback: Fail-safe guarantee
            logger.debug("Observability recording failed silently: %s", type(obs_err).__name__)
        finally:
            # Clean up context variables
            if self._feat_token is not None:
                try:
                    feature_var.reset(self._feat_token)
                except Exception:
                    pass
            if self._op_token is not None:
                try:
                    operation_var.reset(self._op_token)
                except Exception:
                    pass

        # Return False so any original exception is propagated normally
        return False


def observe_ai_operation(
    feature: AIFeature | str,
    operation: str,
    model: str | None = None,
) -> AIOperationObserver:
    """
    Factory function for AIOperationObserver.
    """
    return AIOperationObserver(feature=feature, operation=operation, model=model)
