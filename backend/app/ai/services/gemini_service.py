from __future__ import annotations

import logging
import random
import time
from typing import Any, Callable, TypeVar

from google import genai
from google.genai import errors, types
from pydantic import BaseModel

from app.ai.config import ai_settings
from app.core.observability import (
    AIFeature,
    AIOperationStatus,
    ai_metrics,
    classify_exception,
    get_correlation_id,
)
from app.core.observability.context import record_context_token_usage

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def get_token_limit_for_schema(response_schema: type) -> int:
    """Centralized schema-appropriate max_output_tokens mapping."""
    name = getattr(response_schema, "__name__", "")
    mapping = {
        "ResumeData": ai_settings.resume_parser_max_tokens,
        "CoverLetterResponse": ai_settings.cover_letter_max_tokens,
        "CareerCoachResponse": ai_settings.career_coach_max_tokens,
        "ResumeImprovementAIResult": ai_settings.resume_improvement_max_tokens,
        "ATSAnalysisResult": ai_settings.ats_analyzer_max_tokens,
        "JobDescriptionAIResult": ai_settings.job_description_max_tokens,
        "CandidateEvidenceAIResult": ai_settings.rag_max_tokens,
        "MatchExplanation": ai_settings.match_explanation_max_tokens,
    }
    return mapping.get(name, ai_settings.default_max_output_tokens)


class GeminiService:
    def __init__(self):
        self.client = genai.Client(
            api_key=ai_settings.gemini_api_key,
            http_options=types.HttpOptions(timeout=30.0),
        )

        self.model = ai_settings.gemini_model
        self.fallback_model = ai_settings.gemini_fallback_model

    def _is_retryable_exception(self, exc: Exception) -> bool:
        if isinstance(exc, TimeoutError):
            return True
        if hasattr(errors, "httpx") and isinstance(exc, errors.httpx.TimeoutException):
            return True
        if isinstance(exc, errors.ClientError) and getattr(exc, "code", None) == 429:
            return True
        if isinstance(exc, errors.ServerError) and getattr(exc, "code", None) in (500, 502, 504):
            return True
        return False

    def _execute_with_retry(
        self,
        func: Callable[..., Any],
        *args: Any,
        max_retries: int = 2,
        base_delay: float = 1.0,
        backoff_factor: float = 2.0,
        **kwargs: Any,
    ) -> Any:
        attempts = 0
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                if attempts >= max_retries or not self._is_retryable_exception(exc):
                    raise

                attempts += 1
                delay = base_delay * (backoff_factor ** (attempts - 1)) + random.uniform(0.0, 0.25)
                category, exc_name = classify_exception(exc)
                ai_metrics.record_retry(feature=AIFeature.GEMINI_CLIENT.value)
                logger.warning(
                    "Gemini API transient failure (%s: %s). Retrying attempt %s/%s in %.2fs...",
                    exc_name,
                    category.value,
                    attempts,
                    max_retries,
                    delay,
                    extra={
                        "correlation_id": get_correlation_id(),
                        "feature": AIFeature.GEMINI_CLIENT.value,
                        "retry_attempt": attempts,
                        "error_category": category.value,
                        "exception_type": exc_name,
                    },
                )
                time.sleep(delay)

    def _generate_content(
        self,
        *,
        model: str,
        prompt: str,
        config: dict | None = None,
    ):
        return self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )

    def _extract_and_record_usage(
        self,
        response: Any,
        model: str,
        duration_ms: float,
    ) -> None:
        """
        Extract token usage metadata from Gemini SDK response and record client-level metrics.
        Fails safely if response format or metadata is missing.
        """
        prompt_tokens = None
        completion_tokens = None
        total_tokens = None

        if hasattr(response, "usage_metadata") and response.usage_metadata:
            raw_prompt = getattr(response.usage_metadata, "prompt_token_count", None)
            raw_completion = getattr(response.usage_metadata, "candidates_token_count", None)
            raw_total = getattr(response.usage_metadata, "total_token_count", None)

            prompt_tokens = raw_prompt if isinstance(raw_prompt, int) else None
            completion_tokens = raw_completion if isinstance(raw_completion, int) else None
            total_tokens = raw_total if isinstance(raw_total, int) else None

            if prompt_tokens is not None or completion_tokens is not None:
                record_context_token_usage(prompt_tokens, completion_tokens, total_tokens)

        ai_metrics.record_operation(
            feature=AIFeature.GEMINI_CLIENT.value,
            operation="generate_content",
            status=AIOperationStatus.SUCCESS,
            duration_ms=duration_ms,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )

    def _generate_with_fallback(
        self,
        *,
        prompt: str,
        config: dict | None = None,
    ):
        t0 = time.perf_counter()
        try:
            response = self._execute_with_retry(
                self._generate_content,
                model=self.model,
                prompt=prompt,
                config=config,
            )
            duration_ms = (time.perf_counter() - t0) * 1000.0
            self._extract_and_record_usage(response, self.model, duration_ms)
            return response

        except errors.ServerError as exc:
            if exc.code != 503:
                raise

            if not self.fallback_model or self.fallback_model == self.model:
                raise

            ai_metrics.record_fallback(feature=AIFeature.GEMINI_CLIENT.value)
            logger.warning(
                "Gemini model '%s' is temporarily unavailable (503). Falling back to '%s'.",
                self.model,
                self.fallback_model,
                extra={
                    "correlation_id": get_correlation_id(),
                    "feature": AIFeature.GEMINI_CLIENT.value,
                    "model": self.model,
                    "fallback_model": self.fallback_model,
                },
            )

            t0_fallback = time.perf_counter()
            response = self._execute_with_retry(
                self._generate_content,
                model=self.fallback_model,
                prompt=prompt,
                config=config,
            )
            duration_ms = (time.perf_counter() - t0_fallback) * 1000.0
            self._extract_and_record_usage(response, self.fallback_model, duration_ms)
            return response

    def generate_text(
        self,
        prompt: str,
        max_output_tokens: int | None = None,
    ) -> str:
        tokens = max_output_tokens or ai_settings.default_max_output_tokens
        response = self._generate_with_fallback(
            prompt=prompt,
            config={
                "max_output_tokens": tokens,
            },
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response"
            )

        return response.text

    def generate_structured(
        self,
        prompt: str,
        response_schema: type[T],
        max_output_tokens: int | None = None,
    ) -> T:
        tokens = max_output_tokens or get_token_limit_for_schema(response_schema)
        response = self._generate_with_fallback(
            prompt=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
                "max_output_tokens": tokens,
            },
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response"
            )

        return response_schema.model_validate_json(
            response.text
        )


gemini_service = GeminiService()
