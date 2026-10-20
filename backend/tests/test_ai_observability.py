from __future__ import annotations

import asyncio
from io import StringIO
import json
import logging
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import uuid

import pytest
from fastapi.testclient import TestClient

from app.core.observability.context import (
    get_correlation_id,
    reset_correlation_id,
    set_correlation_id,
    validate_and_sanitize_correlation_id,
)
from app.core.observability.logging import StructuredJsonFormatter
from app.core.observability.metrics import (
    AIMetricsCollector,
    ai_metrics,
    get_ai_metrics_snapshot,
    reset_ai_metrics,
)
from app.core.observability.observer import observe_ai_operation
from app.core.observability.sanitizer import (
    classify_exception,
    sanitize_dict,
    sanitize_text,
)
from app.core.observability.schemas import (
    AIErrorCategory,
    AIFeature,
    AIOperationStatus,
    estimate_token_cost,
)
from app.main import app

client = TestClient(app)


# =============================================================================
# 1. Correlation ID Tests
# =============================================================================

def test_validate_and_sanitize_correlation_id_generates_uuid_when_empty():
    assert len(validate_and_sanitize_correlation_id(None)) == 36
    assert len(validate_and_sanitize_correlation_id("")) == 36
    assert len(validate_and_sanitize_correlation_id("   ")) == 36


def test_validate_and_sanitize_correlation_id_preserves_valid_ids():
    valid_id = "req_12345-abc.XYZ"
    assert validate_and_sanitize_correlation_id(valid_id) == valid_id


def test_validate_and_sanitize_correlation_id_rejects_unsafe_or_long_ids():
    # Length > 64 chars -> replaces with UUID
    too_long = "a" * 65
    result = validate_and_sanitize_correlation_id(too_long)
    assert len(result) == 36
    assert result != too_long

    # Characters that facilitate log injection / header splitting
    with_newline = "valid_id\r\nInjected-Header: evil"
    result = validate_and_sanitize_correlation_id(with_newline)
    assert "\r" not in result
    assert "\n" not in result
    assert len(result) == 36


def test_correlation_id_contextvars_isolation():
    async def worker(worker_id: str):
        cid, token = set_correlation_id(f"req-{worker_id}")
        await asyncio.sleep(0.01)
        assert get_correlation_id() == f"req-{worker_id}"
        reset_correlation_id(token)

    async def main():
        await asyncio.gather(
            worker("task1"),
            worker("task2"),
            worker("task3"),
        )

    asyncio.run(main())


# =============================================================================
# 2. Structured JSON Logging & PII Redaction Tests
# =============================================================================

def test_sanitize_text_redacts_emails_phones_and_credentials():
    raw_text = (
        "User john.doe@example.com with phone +1 (555) 019-2834 used "
        "Bearer eyJhbGciOiJIUzI1NiJ9.test and API key AIzaSyD12345678901234567890123456789012\nNew line"
    )
    sanitized = sanitize_text(raw_text)

    assert "john.doe@example.com" not in sanitized
    assert "[REDACTED_EMAIL]" in sanitized
    assert "555" not in sanitized
    assert "[REDACTED_PHONE]" in sanitized
    assert "eyJhbGciOiJIUzI1NiJ9" not in sanitized
    assert "Bearer [REDACTED_TOKEN]" in sanitized
    assert "AIzaSyD" not in sanitized
    assert "[REDACTED_KEY]" in sanitized
    assert "\n" not in sanitized  # Log injection prevention


def test_sanitize_dict_redacts_sensitive_keys_recursively():
    payload = {
        "user_email": "candidate@example.com",
        "api_key": "secret123",
        "prompt": "Evaluate this candidate resume: Python developer",
        "resume_data": {"phone": "1234567890"},
        "nested": {
            "status": "success",
            "safe_field": "public_data",
        },
    }
    cleaned = sanitize_dict(payload)

    assert cleaned["user_email"] == "[REDACTED]"
    assert cleaned["api_key"] == "[REDACTED]"
    assert cleaned["prompt"] == "[REDACTED]"
    assert cleaned["resume_data"] == "[REDACTED]"
    assert cleaned["nested"]["safe_field"] == "public_data"


def test_structured_json_formatter_outputs_valid_single_line_json():
    formatter = StructuredJsonFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="AI operation completed for candidate",
        args=(),
        exc_info=None,
    )
    record.correlation_id = "test-corr-id-123"
    record.feature = "rag"
    record.duration_ms = 124.5

    formatted = formatter.format(record)
    parsed = json.loads(formatted)

    assert parsed["level"] == "INFO"
    assert parsed["logger"] == "test_logger"
    assert parsed["correlation_id"] == "test-corr-id-123"
    assert parsed["feature"] == "rag"
    assert parsed["duration_ms"] == 124.5
    assert "timestamp" in parsed


# =============================================================================
# 3. Token Metadata Extraction & Cost Estimation Tests
# =============================================================================

def test_estimate_token_cost_calculated_correctly_for_verified_models():
    # gemini-3.5-flash-lite: $0.075/1M input, $0.30/1M output
    cost = estimate_token_cost(
        model="gemini-3.5-flash-lite",
        prompt_tokens=1_000_000,
        completion_tokens=1_000_000,
    )
    assert cost == 0.375

    # gemini-embedding-2: $0.02/1M input, $0.0 output
    embed_cost = estimate_token_cost(
        model="gemini-embedding-2",
        prompt_tokens=500_000,
        completion_tokens=0,
    )
    assert embed_cost == 0.01


def test_estimate_token_cost_returns_none_for_missing_tokens_or_unverified_model():
    assert estimate_token_cost("unknown-model-xyz", 1000, 1000) is None
    assert estimate_token_cost("gemini-3.5-flash-lite", None, 1000) is None
    assert estimate_token_cost("gemini-3.5-flash-lite", -10, 1000) is None


# =============================================================================
# 4. Metrics Collector & Percentile Tests
# =============================================================================

def test_metrics_collector_records_operations_and_bounded_samples():
    collector = AIMetricsCollector()

    for i in range(1200):
        collector.record_operation(
            feature="test_feat",
            operation="test_op",
            status=AIOperationStatus.SUCCESS,
            duration_ms=float(i + 1),
            model="gemini-3.5-flash-lite",
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
        )

    snapshot = collector.get_snapshot()

    # Total requests count equals 1200
    assert snapshot["requests_total"][0]["count"] == 1200

    # Samples are bounded at MAX_LATENCY_SAMPLES (1000)
    lat_stats = snapshot["latencies_ms"]["test_feat:test_op"]
    assert lat_stats["count"] == 1000
    assert lat_stats["min_ms"] == 201.0  # oldest 200 evicted
    assert lat_stats["max_ms"] == 1200.0
    assert lat_stats["p50_ms"] is not None
    assert lat_stats["p95_ms"] is not None

    # Token totals aggregated accurately
    assert snapshot["tokens_total"]["test_feat:prompt"] == 12000
    assert snapshot["tokens_total"]["test_feat:completion"] == 6000
    assert snapshot["tokens_total"]["test_feat:total"] == 18000


def test_metrics_collector_tracks_retries_fallbacks_and_rate_limits():
    collector = AIMetricsCollector()

    collector.record_retry(feature="gemini_client")
    collector.record_retry(feature="gemini_client")
    collector.record_fallback(feature="gemini_client")
    collector.record_rate_limit_rejection()
    collector.record_rag_citations(valid_count=3, invalid_count=1)
    collector.record_rag_chunks_retrieved(4)

    snapshot = collector.get_snapshot()

    assert snapshot["retries_total"]["gemini_client"] == 2
    assert snapshot["fallbacks_total"]["gemini_client"] == 1
    assert snapshot["rate_limit_rejections_total"] == 1
    assert snapshot["rag_telemetry"]["citations_validated"]["valid"] == 3
    assert snapshot["rag_telemetry"]["citations_validated"]["invalid"] == 1
    assert snapshot["rag_telemetry"]["chunks_retrieved_total"] == 4


# =============================================================================
# 5. Error Categorization Tests
# =============================================================================

def test_classify_exception_maps_correctly():
    cat, name = classify_exception(TimeoutError("request timed out"))
    assert cat == AIErrorCategory.TIMEOUT
    assert name == "TimeoutError"

    client_err_429 = SimpleNamespace(code=429)
    cat, _ = classify_exception(client_err_429)  # type: ignore
    assert cat == AIErrorCategory.RATE_LIMIT

    server_err_503 = SimpleNamespace(code=503)
    cat, _ = classify_exception(server_err_503)  # type: ignore
    assert cat == AIErrorCategory.MODEL_UNAVAILABLE

    server_err_500 = SimpleNamespace(code=500)
    cat, _ = classify_exception(server_err_500)  # type: ignore
    assert cat == AIErrorCategory.UPSTREAM_SERVER_ERROR

    val_err = ValueError("Invalid input")
    cat, name = classify_exception(val_err)
    assert cat == AIErrorCategory.VALIDATION_FAILED
    assert name == "ValueError"


# =============================================================================
# 6. Observer Context Manager & Fail-Safe Tests
# =============================================================================

def test_observe_ai_operation_records_success_and_duration():
    reset_ai_metrics()

    with observe_ai_operation(
        feature=AIFeature.RAG,
        operation="test_evidence",
        model="gemini-3.5-flash-lite",
    ) as obs:
        obs.set_token_usage(prompt_tokens=150, completion_tokens=50, total_tokens=200)

    snapshot = get_ai_metrics_snapshot()
    req = [r for r in snapshot["requests_total"] if r["feature"] == "rag"]
    assert len(req) == 1
    assert req[0]["status"] == "success"
    assert req[0]["count"] == 1


def test_observe_ai_operation_records_error_and_propagates_exception():
    reset_ai_metrics()

    with pytest.raises(ValueError, match="Synthetic failure"):
        with observe_ai_operation(
            feature=AIFeature.CAREER_COACH,
            operation="generate",
        ):
            raise ValueError("Synthetic failure")

    snapshot = get_ai_metrics_snapshot()
    errs = [e for e in snapshot["errors_total"] if e["feature"] == "career_coach"]
    assert len(errs) == 1
    assert errs[0]["error_category"] == "validation_failed"


def test_observability_fails_safely_when_internal_error_raised():
    """
    Ensure telemetry failure inside the observer can NEVER mask or disrupt business operations.
    """
    with patch("app.core.observability.observer.ai_metrics.record_operation", side_effect=RuntimeError("Metrics broke")):
        with observe_ai_operation(feature="resilient_test", operation="run"):
            result = 42

        assert result == 42


# =============================================================================
# 7. FastAPI Middleware & HTTP End-to-End Tests
# =============================================================================

def test_correlation_id_middleware_generates_header_if_absent():
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) == 36  # UUID length


def test_correlation_id_middleware_preserves_valid_incoming_header():
    custom_id = "test-client-req-999"
    response = client.get("/health", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == custom_id


def test_correlation_id_middleware_replaces_unsafe_incoming_header():
    unsafe_id = "malicious-id\r\nX-Injected: evil"
    response = client.get("/health", headers={"X-Request-ID": unsafe_id})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] != unsafe_id
    assert len(response.headers["X-Request-ID"]) == 36
