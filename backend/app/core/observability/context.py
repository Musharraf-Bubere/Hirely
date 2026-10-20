from __future__ import annotations

import contextvars
import re
import uuid

# Valid correlation ID pattern: 1-64 characters of alphanumeric, hyphens, underscores, dots.
# Disallows whitespace, newlines (\r, \n), quotes, and control characters to prevent log injection.
CORRELATION_ID_REGEX = re.compile(r"^[a-zA-Z0-9_\-\.]{1,64}$")

correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "hirely_correlation_id", default=""
)
feature_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "hirely_current_feature", default=""
)
operation_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "hirely_current_operation", default=""
)

# Ephemeral storage for token usage from the most recent Gemini call in this context
token_usage_var: contextvars.ContextVar[tuple[int | None, int | None, int | None] | None] = contextvars.ContextVar(
    "hirely_token_usage", default=None
)


def validate_and_sanitize_correlation_id(raw_id: str | None) -> str:
    """
    Validate and sanitize an incoming correlation/request ID.
    Enforces a strict length bound (1-64 chars) and character set to prevent
    log injection, header splitting, and memory attacks.
    Generates a fresh UUID4 if the input is None, empty, whitespace, or invalid.
    """
    if not raw_id:
        return str(uuid.uuid4())

    cleaned = raw_id.strip()
    if not cleaned or not CORRELATION_ID_REGEX.match(cleaned):
        return str(uuid.uuid4())

    return cleaned


def get_correlation_id() -> str:
    """
    Retrieve the active correlation ID for the current context.
    If none is set, generates and sets a fresh UUID4.
    """
    cid = correlation_id_var.get()
    if not cid:
        cid = str(uuid.uuid4())
        correlation_id_var.set(cid)
    return cid


def set_correlation_id(raw_id: str | None) -> tuple[str, contextvars.Token[str]]:
    """
    Validate and set the correlation ID in the current execution context.
    Returns (sanitized_correlation_id, context_reset_token).
    """
    sanitized = validate_and_sanitize_correlation_id(raw_id)
    token = correlation_id_var.set(sanitized)
    return sanitized, token


def reset_correlation_id(token: contextvars.Token[str]) -> None:
    """
    Reset correlation ID to its prior context state.
    """
    try:
        correlation_id_var.reset(token)
    except Exception:
        pass


def record_context_token_usage(
    prompt_tokens: int | None,
    completion_tokens: int | None,
    total_tokens: int | None,
) -> None:
    token_usage_var.set((prompt_tokens, completion_tokens, total_tokens))


def pop_context_token_usage() -> tuple[int | None, int | None, int | None] | None:
    usage = token_usage_var.get()
    token_usage_var.set(None)
    return usage
