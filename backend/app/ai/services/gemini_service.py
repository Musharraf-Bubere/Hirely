from typing import TypeVar

from google import genai
from google.genai import errors
from pydantic import BaseModel

from app.ai.config import ai_settings


T = TypeVar("T", bound=BaseModel)


class GeminiService:
    def __init__(self):
        self.client = genai.Client(
            api_key=ai_settings.gemini_api_key
        )

        self.model = ai_settings.gemini_model
        self.fallback_model = ai_settings.gemini_fallback_model

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
            return self._generate_content(
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

            print(
                f"Gemini model '{self.model}' is temporarily unavailable. "
                f"Falling back to '{self.fallback_model}'."
            )

            return self._generate_content(
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