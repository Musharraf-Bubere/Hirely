import math

from app.ai.embeddings.service import EmbeddingService, embedding_service
from app.ai.matching.similarity import cosine_similarity
from app.ai.rag.schemas import EvidenceChunk


DEFAULT_RELEVANCE_THRESHOLD = 0.45


class CandidateEvidenceRetriever:
    """
    Ranks and retrieves the most relevant candidate resume evidence chunks
    for a recruiter query using semantic embeddings and cosine similarity.

    Characteristics:
    - Pure in-memory similarity computation over candidate's bounded chunk set (10-30 chunks).
    - Configurable similarity threshold (default 0.45) to discard unrelated chunks.
    - Zero external vector database requirement.
    - Graceful handling of empty, sparse, or anomalous chunk vectors.
    """

    def __init__(
        self,
        embedding_svc: EmbeddingService | None = None,
        default_threshold: float = DEFAULT_RELEVANCE_THRESHOLD,
    ):
        self.embedding_service = embedding_svc or embedding_service
        self.default_threshold = default_threshold

    def _prepare_chunk_text(self, chunk: EvidenceChunk) -> str:
        parts = [f"Section: {chunk.section}"]
        if chunk.title:
            parts.append(f"Title: {chunk.title}")
        if chunk.organization:
            parts.append(f"Organization: {chunk.organization}")
        if chunk.timeframe:
            parts.append(f"Timeframe: {chunk.timeframe}")
        parts.append(f"Content: {chunk.content}")
        return "\n".join(parts)

    def retrieve(
        self,
        *,
        query: str,
        chunks: list[EvidenceChunk],
        top_k: int = 4,
        threshold: float | None = None,
    ) -> list[tuple[EvidenceChunk, float]]:
        """
        Embeds the query and candidate chunks, computes pairwise cosine similarity,
        filters by minimum relevance threshold, and returns the top-k scored chunks.
        """
        if not query or not query.strip():
            raise ValueError("Query string cannot be empty.")

        if not chunks:
            return []

        active_threshold = threshold if threshold is not None else self.default_threshold
        query_text = query.strip()

        # 1. Embed query
        query_vector = self.embedding_service.embed_text(query_text)
        if not query_vector or any(not math.isfinite(x) for x in query_vector):
            raise RuntimeError("Failed to generate valid query embedding.")

        if all(x == 0.0 for x in query_vector):
            raise RuntimeError("Query embedding has zero magnitude.")

        # 2. Score candidate chunks
        scored_chunks: list[tuple[EvidenceChunk, float]] = []

        for chunk in chunks:
            chunk_text = self._prepare_chunk_text(chunk)
            try:
                chunk_vector = self.embedding_service.embed_text(chunk_text)
                if not chunk_vector:
                    continue
                if len(chunk_vector) != len(query_vector):
                    # Dimensionality mismatch: safely ignore incompatible chunk
                    continue
                sim = cosine_similarity(query_vector, chunk_vector)
                if not math.isfinite(sim):
                    continue
            except (ValueError, TypeError, ZeroDivisionError):
                # Safely discard zero-magnitude or malformed vectors
                continue

            if sim >= active_threshold:
                scored_chunks.append((chunk, float(sim)))

        # 3. Sort by score descending and take top_k
        scored_chunks.sort(key=lambda x: x[1], reverse=True)

        return scored_chunks[:top_k]


candidate_evidence_retriever = CandidateEvidenceRetriever()
