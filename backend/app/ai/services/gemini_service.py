from typing import TypeVar

from google import genai
from pydantic import BaseModel

from app.ai.config import ai_settings

T = TypeVar("T", bound=BaseModel)

class GeminiService:
    def __init__(self):
        self.client = genai.Client(
            api_key=ai_settings.gemini_api_key
        )
        self.model = ai_settings.gemini_model

    def generate_text(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response")

        return response.text

    def generate_structured(
            self,
            prompt: str,
            response_schema: type[T],
    ) -> T:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_schema,
            }
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response")

        return response_schema.model_validate_json(response.text)


gemini_service = GeminiService()