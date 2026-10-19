import logging
import random
import time
from typing import Any, Callable, TypeVar

from google import genai
from google.genai import errors, types
from pydantic import BaseModel

from app.ai.config import ai_settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


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
                logger.warning(
                    "Gemini API transient failure (%s: %s). Retrying attempt %s/%s in %.2fs...",
                    type(exc).__name__,
                    exc,
                    attempts,
                    max_retries,
                    delay,
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

    def _generate_with_fallback(
        self,
        *,
        prompt: str,
        config: dict | None = None,
    ):
        try:
            return self._execute_with_retry(
                self._generate_content,
                model=self.model,
                prompt=prompt,
                config=config,
            )

        except errors.ServerError as exc:
            if exc.code != 503:
                raise

            if not self.fallback_model:
                raise

            if self.fallback_model == self.model:
                raise

            logger.warning(
                "Gemini model '%s' is temporarily unavailable (503). Falling back to '%s'.",
                self.model,
                self.fallback_model,
            )

            return self._execute_with_retry(
                self._generate_content,
                model=self.fallback_model,
                prompt=prompt,
                config=config,
            )

    def generate_text(self, prompt: str) -> str:
        response = self._generate_with_fallback(
            prompt=prompt
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
    ) -> T:
        response = self._generate_with_fallback(
            prompt=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
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