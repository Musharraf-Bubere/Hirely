from __future__ import annotations

import re
from typing import Any

from app.core.observability.schemas import AIErrorCategory

# Regex patterns for defense-in-depth redaction
EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    re.IGNORECASE,
)
PHONE_PATTERN = re.compile(
    r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
)
BEARER_PATTERN = re.compile(
    r"Bearer\s+[A-Za-z0-9\-._~+/]+=*",
    re.IGNORECASE,
)
API_KEY_PATTERN = re.compile(
    r"(?:AIza[0-9A-Za-z-_]{35}|[0-9a-f]{32}|[0-9a-f]{64})",
    re.IGNORECASE,
)

SENSITIVE_KEY_SUBSTRINGS = (
    "password",
    "token",
    "secret",
    "key",
    "authorization",
    "email",
    "phone",
    "credential",
    "prompt",
    "resume",
)


def sanitize_text(text: str) -> str:
    """
    Scrub common PII and credentials from a string for defense-in-depth logging.
    Preserves log utility while preventing accidental token/email/phone leakage.
    """
    if not text:
        return text

    sanitized = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", text)
    sanitized = BEARER_PATTERN.sub("Bearer [REDACTED_TOKEN]", sanitized)
    sanitized = API_KEY_PATTERN.sub("[REDACTED_KEY]", sanitized)
    sanitized = PHONE_PATTERN.sub("[REDACTED_PHONE]", sanitized)
    # Strip carriage returns and newlines to eliminate log injection risks
    sanitized = sanitized.replace("\r", " ").replace("\n", " ")
    return sanitized.strip()


def sanitize_dict(data: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively sanitize dictionary values and remove sensitive keys.
    """
    sanitized: dict[str, Any] = {}
    for key, value in data.items():
        key_lower = str(key).lower()
        if any(substr in key_lower for substr in SENSITIVE_KEY_SUBSTRINGS):
            sanitized[key] = "[REDACTED]"
            continue

        if isinstance(value, str):
            sanitized[key] = sanitize_text(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, (list, tuple)):
            sanitized[key] = [
                sanitize_text(v) if isinstance(v, str) else v
                for v in value
            ]
        else:
            sanitized[key] = value

    return sanitized


def classify_exception(exc: Exception | None) -> tuple[AIErrorCategory, str]:
    """
    Map an exception to a safe, controlled error category and exception class name.
    Strictly avoids exposing raw exception messages or private internals.
    """
    if exc is None:
        return AIErrorCategory.UNKNOWN, "None"

    exc_class_name = type(exc).__name__

    # 1. Timeout detection
    if isinstance(exc, TimeoutError):
        return AIErrorCategory.TIMEOUT, exc_class_name

    module_name = getattr(type(exc), "__module__", "")
    if "httpx" in module_name and "Timeout" in exc_class_name:
        return AIErrorCategory.TIMEOUT, exc_class_name

    # 2. Google GenAI / HTTP Client / Server error detection
    status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)

    if status_code == 429:
        return AIErrorCategory.RATE_LIMIT, exc_class_name
    if status_code in (401, 403):
        return AIErrorCategory.AUTHENTICATION, exc_class_name
    if status_code == 503:
        return AIErrorCategory.MODEL_UNAVAILABLE, exc_class_name
    if status_code in (500, 502, 504):
        return AIErrorCategory.UPSTREAM_SERVER_ERROR, exc_class_name
    if status_code == 400:
        return AIErrorCategory.CLIENT_ERROR, exc_class_name

    # 3. Validation / Parsing errors
    if "ValidationError" in exc_class_name:
        return AIErrorCategory.VALIDATION_FAILED, exc_class_name
    if isinstance(exc, ValueError):
        return AIErrorCategory.VALIDATION_FAILED, exc_class_name

    # 4. Citation specific errors
    if "Citation" in exc_class_name:
        return AIErrorCategory.CITATION_INVALID, exc_class_name

    return AIErrorCategory.INTERNAL_ERROR, exc_class_name
