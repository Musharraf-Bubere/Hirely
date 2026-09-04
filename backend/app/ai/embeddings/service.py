from google import genai
from google.genai import types

from app.ai.config import ai_settings


class EmbeddingService:
    def __init__(self):
        self.client = genai.Client(
            api_key=ai_settings.gemini_api_key
        )

        self.model = "gemini-embedding-2"
        self.output_dimensionality = 768

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty")

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=self.output_dimensionality
            ),
        )

        if not response.embeddings:
            raise RuntimeError("Gemini returned no embeddings")

        embedding = response.embeddings[0]

        if not embedding.values:
            raise RuntimeError("Gemini returned an empty embedding")

        return list(embedding.values)


embedding_service = EmbeddingService()