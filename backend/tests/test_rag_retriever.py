from unittest.mock import MagicMock

import pytest

from app.ai.rag.retriever import CandidateEvidenceRetriever
from app.ai.rag.schemas import EvidenceChunk


def make_test_chunks() -> list[EvidenceChunk]:
    return [
        EvidenceChunk(
            chunk_id="exp_0",
            section="experience",
            title="Database Engineer",
            organization="DataTech",
            timeframe="2020 - Present",
            content="Managed and scaled PostgreSQL cluster with 10TB data, optimizing queries and replication.",
        ),
        EvidenceChunk(
            chunk_id="exp_1",
            section="experience",
            title="Frontend Developer",
            organization="WebStudio",
            timeframe="2018 - 2020",
            content="Built responsive user interfaces using React, Redux, and CSS modules.",
        ),
        EvidenceChunk(
            chunk_id="edu_0",
            section="education",
            title="B.Tech",
            organization="Anna University",
            timeframe="2014 - 2018",
            content="Bachelor of Technology in Information Technology.",
        ),
        EvidenceChunk(
            chunk_id="cert_0",
            section="certifications",
            title="AWS Certified Database Specialist",
            organization="Amazon Web Services",
            timeframe="2022",
            content="Certification for relational and NoSQL database design on AWS RDS and DynamoDB.",
        ),
    ]


def test_retriever_query_validation():
    retriever = CandidateEvidenceRetriever()
    with pytest.raises(ValueError, match="cannot be empty"):
        retriever.retrieve(query="", chunks=[])
    with pytest.raises(ValueError, match="cannot be empty"):
        retriever.retrieve(query="   ", chunks=[])


def test_retriever_empty_chunks():
    mock_embedding_svc = MagicMock()
    retriever = CandidateEvidenceRetriever(embedding_svc=mock_embedding_svc)
    results = retriever.retrieve(query="database experience", chunks=[])
    assert results == []
    mock_embedding_svc.embed_text.assert_not_called()


def test_retriever_ranks_relevant_chunks_above_unrelated():
    """
    Controlled embedding test:
    Vector space: [DB_relevance, Frontend_relevance, Other]
    Query: Database optimization -> [0.95, 0.05, 0.0]
    Chunk 0 (PostgreSQL): [0.90, 0.10, 0.0]  -> Cosine ~ 0.99 (High match)
    Chunk 1 (React Frontend): [0.05, 0.95, 0.0] -> Cosine ~ 0.10 (Low match)
    Chunk 2 (Education): [0.10, 0.10, 0.80]  -> Cosine ~ 0.12 (Low match)
    Chunk 3 (AWS DB Cert): [0.85, 0.05, 0.20]-> Cosine ~ 0.96 (High match)
    """
    chunks = make_test_chunks()

    def mock_embed(text: str) -> list[float]:
        text_lower = text.lower()
        if "database optimization" in text_lower:
            return [0.95, 0.05, 0.0]
        if "aws certified database" in text_lower or "nosql" in text_lower:
            return [0.85, 0.05, 0.20]
        if "postgresql" in text_lower or "managed and scaled" in text_lower:
            return [0.90, 0.10, 0.0]
        if "react" in text_lower or "frontend" in text_lower:
            return [0.05, 0.95, 0.0]
        if "anna university" in text_lower or "bachelor" in text_lower:
            return [0.10, 0.10, 0.80]
        return [0.0, 0.0, 1.0]

    mock_embedding_svc = MagicMock()
    mock_embedding_svc.embed_text.side_effect = mock_embed

    retriever = CandidateEvidenceRetriever(embedding_svc=mock_embedding_svc, default_threshold=0.45)
    results = retriever.retrieve(query="database optimization", chunks=chunks, top_k=4)

    # Must retrieve top chunks above 0.45 threshold
    assert len(results) >= 2
    top_chunk, top_score = results[0]
    second_chunk, second_score = results[1]

    assert top_chunk.chunk_id == "exp_0"
    assert "PostgreSQL" in top_chunk.content
    assert top_score > 0.90

    assert second_chunk.chunk_id == "cert_0"
    assert "AWS Certified Database" in second_chunk.title
    assert "NoSQL" in second_chunk.content
    assert second_score > 0.80


def test_retriever_discards_unrelated_queries_below_threshold():
    """Unrelated queries (e.g. baking, piloting) score below 0.45 and return zero chunks."""
    chunks = make_test_chunks()

    def mock_embed(text: str) -> list[float]:
        if "baking sourdough" in text.lower():
            return [0.0, 0.0, 1.0]
        # Chunks are orthogonal to baking
        return [1.0, 0.0, 0.0]

    mock_embedding_svc = MagicMock()
    mock_embedding_svc.embed_text.side_effect = mock_embed

    retriever = CandidateEvidenceRetriever(embedding_svc=mock_embedding_svc, default_threshold=0.45)
    results = retriever.retrieve(query="baking sourdough bread", chunks=chunks)

    assert results == []


def test_retriever_respects_top_k():
    chunks = make_test_chunks()

    mock_embedding_svc = MagicMock()
    # Identical vectors -> all chunks get similarity 1.0
    mock_embedding_svc.embed_text.return_value = [1.0, 1.0, 1.0]

    retriever = CandidateEvidenceRetriever(embedding_svc=mock_embedding_svc, default_threshold=0.0)
    results = retriever.retrieve(query="skills", chunks=chunks, top_k=2)

    assert len(results) == 2


# =====================================================================
# Documented Evaluation Set: Retrieval Relevance & Evidence Targeting
# =====================================================================

EVALUATION_CASES = [
    {
        "query": "PostgreSQL database clustering and replication",
        "expected_top_section": "experience",
        "expected_top_chunk_id": "exp_0",
    },
    {
        "query": "AWS cloud database certification",
        "expected_top_section": "certifications",
        "expected_top_chunk_id": "cert_0",
    },
    {
        "query": "Frontend user interface engineering with React",
        "expected_top_section": "experience",
        "expected_top_chunk_id": "exp_1",
    },
    {
        "query": "University degree and academic background",
        "expected_top_section": "education",
        "expected_top_chunk_id": "edu_0",
    },
]


@pytest.mark.parametrize("eval_case", EVALUATION_CASES)
def test_documented_evaluation_cases(eval_case):
    chunks = make_test_chunks()

    def mock_embed(text: str) -> list[float]:
        t = text.lower()
        if "postgresql" in t or "cluster" in t or "replication" in t:
            return [1.0, 0.0, 0.0, 0.0]
        if "aws" in t or "certification" in t or "nosql" in t:
            return [0.0, 1.0, 0.0, 0.0]
        if "react" in t or "frontend" in t or "css" in t:
            return [0.0, 0.0, 1.0, 0.0]
        if "degree" in t or "university" in t or "bachelor" in t:
            return [0.0, 0.0, 0.0, 1.0]
        return [0.25, 0.25, 0.25, 0.25]

    mock_embedding_svc = MagicMock()
    mock_embedding_svc.embed_text.side_effect = mock_embed

    retriever = CandidateEvidenceRetriever(embedding_svc=mock_embedding_svc, default_threshold=0.45)
    results = retriever.retrieve(query=eval_case["query"], chunks=chunks, top_k=1)

    assert len(results) == 1
    top_chunk, score = results[0]
    assert top_chunk.chunk_id == eval_case["expected_top_chunk_id"]
    assert top_chunk.section == eval_case["expected_top_section"]
    assert score > 0.90


def test_retriever_handles_dimension_mismatch_safely():
    """If a chunk embedding returns mismatched dimensionality, it is skipped without crashing."""
    chunks = make_test_chunks()

    def mock_embed(text: str) -> list[float]:
        if "postgresql" in text.lower():
            return [1.0, 0.0]  # Incompatible dimension (2 elements instead of 3)
        return [1.0, 0.0, 0.0]

    mock_embedding_svc = MagicMock()
    mock_embedding_svc.embed_text.side_effect = mock_embed

    retriever = CandidateEvidenceRetriever(embedding_svc=mock_embedding_svc, default_threshold=0.45)
    # Query returns 3-dimensional vector
    results = retriever.retrieve(query="database query", chunks=chunks, top_k=4)

    # Incompatible chunk (exp_0) was skipped safely, remaining compatible chunks evaluated
    retrieved_ids = [c.chunk_id for c, _ in results]
    assert "exp_0" not in retrieved_ids


def test_retriever_handles_zero_magnitude_vector_safely():
    """If a chunk returns all zeros (zero magnitude), cosine similarity error is caught and skipped."""
    chunks = make_test_chunks()

    def mock_embed(text: str) -> list[float]:
        if "postgresql" in text.lower():
            return [0.0, 0.0, 0.0]  # Zero magnitude vector
        return [0.8, 0.2, 0.0]

    mock_embedding_svc = MagicMock()
    mock_embedding_svc.embed_text.side_effect = mock_embed

    retriever = CandidateEvidenceRetriever(embedding_svc=mock_embedding_svc, default_threshold=0.45)
    results = retriever.retrieve(query="database query", chunks=chunks, top_k=4)

    retrieved_ids = [c.chunk_id for c, _ in results]
    assert "exp_0" not in retrieved_ids


def test_retriever_handles_non_finite_vector_safely():
    """If a chunk returns non-finite float values (NaN/Inf), it is skipped safely."""
    chunks = make_test_chunks()

    def mock_embed(text: str) -> list[float]:
        if "postgresql" in text.lower():
            return [float("nan"), 0.0, 0.0]  # Non-finite vector
        return [0.8, 0.2, 0.0]

    mock_embedding_svc = MagicMock()
    mock_embedding_svc.embed_text.side_effect = mock_embed

    retriever = CandidateEvidenceRetriever(embedding_svc=mock_embedding_svc, default_threshold=0.45)
    results = retriever.retrieve(query="database query", chunks=chunks, top_k=4)

    retrieved_ids = [c.chunk_id for c, _ in results]
    assert "exp_0" not in retrieved_ids


def test_retriever_rejects_zero_magnitude_query_vector():
    """If the query embedding itself has zero magnitude, raises RuntimeError."""
    chunks = make_test_chunks()
    mock_embedding_svc = MagicMock()
    mock_embedding_svc.embed_text.return_value = [0.0, 0.0, 0.0]

    retriever = CandidateEvidenceRetriever(embedding_svc=mock_embedding_svc)
    with pytest.raises(RuntimeError, match="zero magnitude"):
        retriever.retrieve(query="empty query test", chunks=chunks)
