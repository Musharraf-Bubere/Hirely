from google import genai

from app.ai.config import ai_settings


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


gemini_service = GeminiService()