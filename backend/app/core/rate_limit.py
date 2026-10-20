"""
In-memory sliding-window rate limiter for expensive AI endpoints.

NOTE: This rate limiter is process-local and designed for single-worker
deployments. In multi-worker or distributed production environments,
a Redis-backed sliding-window rate limiter should be used.
"""

from collections import defaultdict, deque
import logging
import threading
import time
from typing import DefaultDict

from fastapi import Depends, HTTPException, status

from app.api.dependencies import get_current_user
from app.core.observability import AIFeature, ai_metrics, get_correlation_id
from app.models.user import User

logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    """
    Thread-safe sliding-window in-memory rate limiter using deques.
    """

    def __init__(self, max_requests: int = 30, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._requests: DefaultDict[str, deque[float]] = defaultdict(deque)

    def is_allowed(self, key: str, now: float | None = None) -> tuple[bool, int]:
        """
        Check if the request for `key` is allowed within the sliding window.

        Returns:
            (allowed: bool, retry_after_seconds: int)
        """
        if now is None:
            now = time.time()

        window_start = now - self.window_seconds

        with self._lock:
            timestamps = self._requests[key]

            # Evict timestamps older than the sliding window
            while timestamps and timestamps[0] <= window_start:
                timestamps.popleft()

            if len(timestamps) < self.max_requests:
                timestamps.append(now)
                return True, 0

            oldest = timestamps[0]
            retry_after = max(1, int(oldest + self.window_seconds - now + 0.999))
            return False, retry_after

    def reset(self, key: str | None = None) -> None:
        """
        Reset timestamps for a specific key or all keys (useful for test isolation).
        """
        with self._lock:
            if key is not None:
                self._requests.pop(key, None)
            else:
                self._requests.clear()


ai_rate_limiter = InMemoryRateLimiter(max_requests=30, window_seconds=60.0)


def check_ai_rate_limit(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    FastAPI dependency enforcing per-user sliding-window rate limit on AI endpoints.
    Emits privacy-preserving telemetry on rejection without exposing user identifiers.
    """
    allowed, retry_after = ai_rate_limiter.is_allowed(str(current_user.id))
    if not allowed:
        ai_metrics.record_rate_limit_rejection()
        logger.warning(
            "AI request rate limit exceeded",
            extra={
                "correlation_id": get_correlation_id(),
                "feature": AIFeature.RATE_LIMITER.value,
                "retry_after": retry_after,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="AI request rate limit exceeded. Please wait before submitting more inquiries.",
            headers={"Retry-After": str(retry_after)},
        )
    return current_user
