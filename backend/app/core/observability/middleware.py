from __future__ import annotations

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.observability.context import (
    reset_correlation_id,
    set_correlation_id,
)
from app.core.observability.metrics import ai_metrics
from app.core.observability.schemas import AIFeature, AIOperationStatus


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    FastAPI / Starlette middleware enforcing end-to-end request correlation.
    - Validates incoming 'X-Request-ID' or 'X-Correlation-ID' header.
    - Falls back to a clean UUID4 if missing or containing invalid/unsafe characters.
    - Propagates correlation ID through Python contextvars across async tasks.
    - Injects 'X-Request-ID' into the outgoing response headers.
    - Records high-level HTTP request timing and status metrics.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        raw_correlation_id = (
            request.headers.get("x-request-id")
            or request.headers.get("x-correlation-id")
        )

        correlation_id, token = set_correlation_id(raw_correlation_id)
        start_time = time.perf_counter()

        try:
            response: Response = await call_next(request)
            duration_ms = (time.perf_counter() - start_time) * 1000.0

            # Attach verified correlation ID to outgoing response headers
            response.headers["X-Request-ID"] = correlation_id

            # Record high-level HTTP status metric with low-cardinality method and status
            status_tag = (
                AIOperationStatus.SUCCESS.value
                if response.status_code < 400
                else AIOperationStatus.ERROR.value
            )
            ai_metrics.record_operation(
                feature=AIFeature.HTTP_REQUEST.value,
                operation=request.method,
                status=status_tag,
                duration_ms=duration_ms,
            )

            return response

        finally:
            reset_correlation_id(token)
