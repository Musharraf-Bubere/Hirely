import pytest

from app.ai.embeddings.service import EmbeddingService
from app.ai.matching.similarity import cosine_similarity


@pytest.mark.integration
def test_semantically_similar_texts_have_higher_similarity():
    embedding_service = EmbeddingService()

    candidate_text = """
    Python backend developer with experience in FastAPI,
    PostgreSQL, REST APIs, and Docker.
    """

    matching_job_text = """
    Backend engineer needed with strong Python,
    FastAPI, PostgreSQL, REST API, and Docker experience.
    """

    unrelated_job_text = """
    Graphic designer experienced in Photoshop,
    Illustrator, branding, and visual design.
    """

    candidate_embedding = embedding_service.embed_text(
        candidate_text
    )

    matching_job_embedding = embedding_service.embed_text(
        matching_job_text
    )

    unrelated_job_embedding = embedding_service.embed_text(
        unrelated_job_text
    )

    matching_similarity = cosine_similarity(
        candidate_embedding,
        matching_job_embedding,
    )

    unrelated_similarity = cosine_similarity(
        candidate_embedding,
        unrelated_job_embedding,
    )

    print(f"Matching similarity: {matching_similarity}")
    print(f"Unrelated similarity: {unrelated_similarity}")

    assert len(candidate_embedding) == 768
    assert len(matching_job_embedding) == 768
    assert len(unrelated_job_embedding) == 768

    assert matching_similarity > unrelated_similarity