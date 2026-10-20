from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.rate_limit import (
    InMemoryRateLimiter,
    auth_rate_limiter,
    check_auth_rate_limit,
    get_client_ip,
)
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.core.security import create_access_token, hash_password


def test_in_memory_rate_limiter_threshold_and_recovery():
    limiter = InMemoryRateLimiter(max_requests=3, window_seconds=10.0)

    # First 3 requests at t=100.0 allowed
    allowed, retry_after = limiter.is_allowed("client-1", now=100.0)
    assert allowed is True
    assert retry_after == 0

    allowed, retry_after = limiter.is_allowed("client-1", now=101.0)
    assert allowed is True

    allowed, retry_after = limiter.is_allowed("client-1", now=102.0)
    assert allowed is True

    # 4th request at t=103.0 rejected
    allowed, retry_after = limiter.is_allowed("client-1", now=103.0)
    assert allowed is False
    assert retry_after == 7  # 100.0 + 10.0 - 103.0 = 7 seconds

    # Distinct client at t=103.0 allowed
    allowed_c2, _ = limiter.is_allowed("client-2", now=103.0)
    assert allowed_c2 is True

    # Client-1 recovers after window expires (t=111.0)
    allowed, retry_after = limiter.is_allowed("client-1", now=111.0)
    assert allowed is True
    assert retry_after == 0


def test_in_memory_rate_limiter_bounded_memory_eviction():
    limiter = InMemoryRateLimiter(max_requests=2, window_seconds=5.0, max_keys=3)

    # Fill to capacity at t=10.0
    limiter.is_allowed("key1", now=10.0)
    limiter.is_allowed("key2", now=10.0)
    limiter.is_allowed("key3", now=10.0)

    # At t=20.0 (past window), adding key4 purges stale keys
    limiter.is_allowed("key4", now=20.0)
    assert len(limiter._requests) <= 3


def test_get_client_ip_proxy_trust_behavior():
    # 1. Untrusted proxy (default settings): ignores X-Forwarded-For
    mock_request = MagicMock(spec=Request)
    mock_request.client.host = "192.168.1.50"
    mock_request.headers.get.return_value = "203.0.113.195, 70.41.3.18"

    original_trust = settings.trust_proxy_headers
    try:
        settings.trust_proxy_headers = False
        ip = get_client_ip(mock_request)
        assert ip == "192.168.1.50"

        # 2. Trusted proxy enabled: extracts leftmost client IP
        settings.trust_proxy_headers = True
        ip_trusted = get_client_ip(mock_request)
        assert ip_trusted == "203.0.113.195"
    finally:
        settings.trust_proxy_headers = original_trust


def test_get_client_ip_fallback_when_client_is_none():
    mock_request = MagicMock(spec=Request)
    mock_request.client = None
    mock_request.headers.get.return_value = None

    ip = get_client_ip(mock_request)
    assert ip == "unknown_client"


def test_auth_rate_limit_endpoint_blocks_brute_force():
    from app.main import app
    client = TestClient(app)

    auth_rate_limiter.reset()

    try:
        # Send 10 login attempts (allowed by limiter, even if credentials fail)
        for i in range(10):
            resp = client.post(
                "/auth/login",
                json={"email": f"nonexistent_{i}@example.com", "password": "WrongPassword123!"},
            )
            assert resp.status_code == 401

        # 11th request must be rejected with 429
        resp11 = client.post(
            "/auth/login",
            json={"email": "nonexistent_11@example.com", "password": "WrongPassword123!"},
        )
        assert resp11.status_code == 429
        assert "Too many authentication requests" in resp11.json()["detail"]
        assert "Retry-After" in resp11.headers

    finally:
        auth_rate_limiter.reset()
