from __future__ import annotations

from datetime import datetime, timezone
import json
import logging
import sys
from typing import Any

from app.core.observability.context import (
    get_correlation_id,
    feature_var,
    operation_var,
)
from app.core.observability.sanitizer import sanitize_dict, sanitize_text


class StructuredJsonFormatter(logging.Formatter):
    """
    Production-grade JSON log formatter for Hirely.
    Outputs single-line valid JSON records enriched with correlation IDs
    and sanitized against PII, prompt leaks, and credentials.
    """

    def format(self, record: logging.LogRecord) -> str:
        # Standard base log payload
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": sanitize_text(record.getMessage()),
            "correlation_id": getattr(
                record, "correlation_id", None
            ) or get_correlation_id(),
        }

        # Include contextual feature/operation if set
        feature = getattr(record, "feature", None) or feature_var.get()
        if feature:
            log_entry["feature"] = str(feature)

        operation = getattr(record, "operation", None) or operation_var.get()
        if operation:
            log_entry["operation"] = str(operation)

        # Include structured event extras if supplied
        event_fields = (
            "duration_ms",
            "model",
            "status",
            "error_category",
            "exception_type",
            "tokens",
            "retry_attempt",
            "fallback_model",
            "chunks_count",
            "citations_valid",
        )
        for field in event_fields:
            if hasattr(record, field):
                log_entry[field] = getattr(record, field)

        # Defense-in-depth sanitization of the final dictionary
        sanitized_entry = sanitize_dict(log_entry)

        # Output single-line JSON string
        try:
            return json.dumps(sanitized_entry, ensure_ascii=False)
        except Exception:
            # Fallback formatting if serialization fails
            return json.dumps({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": "[FALLBACK_LOG_SERIALIZATION_FAILED]",
                "correlation_id": get_correlation_id(),
            })


def setup_observability(
    logger_name: str = "app",
    level: int = logging.INFO,
    json_format: bool = True,
) -> None:
    """
    Initialize structured logging for Hirely.
    Fails safely so logging configuration cannot disrupt server startup.
    """
    try:
        target_logger = logging.getLogger(logger_name)
        target_logger.setLevel(level)

        # Remove existing stream handlers to avoid duplicate log lines
        for handler in list(target_logger.handlers):
            if isinstance(handler, logging.StreamHandler):
                target_logger.removeHandler(handler)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        if json_format:
            handler.setFormatter(StructuredJsonFormatter())
        else:
            handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s] %(levelname)s [%(name)s] %(message)s"
                )
            )

        target_logger.addHandler(handler)
    except Exception as exc:
        # Never let logging setup break app initialization
        sys.stderr.write(f"Warning: Failed to setup structured observability: {exc}\n")
