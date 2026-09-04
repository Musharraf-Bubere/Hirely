from types import SimpleNamespace

import pytest

from app.ai.embeddings.service import EmbeddingService


class FakeEmbeddingsClient:
    def embed_content(self, **kwargs):
        return SimpleNamespace(
            embeddings=[
                SimpleNamespace(
                    values=[0.1, 0.2, 0.3]
                )
            ]
        )


class FakeGeminiClient:
    def __init__(self):
        self.models = FakeEmbeddingsClient()


def test_embed_text_returns_embedding():
    service = EmbeddingService()

    service.client = FakeGeminiClient()

    result = service.embed_text(
        "Python backend developer with FastAPI experience."
    )

    assert isinstance(result, list)
    assert result == [0.1, 0.2, 0.3]


def test_embed_text_rejects_empty_text():
    service = EmbeddingService()

    with pytest.raises(ValueError, match="Text cannot be empty"):
        service.embed_text("")