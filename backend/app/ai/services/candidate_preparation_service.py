from __future__ import annotations

from collections import OrderedDict, defaultdict
import hashlib
import logging
import threading
from typing import DefaultDict
from uuid import UUID

from pydantic import BaseModel

from app.ai.embeddings.service import EmbeddingService, embedding_service
from app.ai.parsers.schemas import ResumeData
from app.ai.representations.candidate import (
    CandidateRepresentation,
    CandidateRepresentationBuilder,
    candidate_representation_builder,
)

logger = logging.getLogger(__name__)


class CandidateEmbeddingCache:
    """
    Thread-safe, bounded in-process LRU cache for candidate profile embeddings.

    Prevents expensive repeated calls to the Gemini embedding API for unchanged candidate
    profile representations during recruiter matching and candidate matching workflows.

    Architecture & Eviction Policy:
        - Bounded size (default max_size=1000 items, ~6 MB RAM at 768 float dimensions).
        - Least-Recently-Used (LRU) eviction implemented via collections.OrderedDict.
        - Process-local in-memory storage (does not persist across process restarts
          or synchronize across independent multi-process workers).

    Key Computation & Invalidation Strategy:
        - Content-addressable key: SHA-256 hash of (candidate_id, model_name, profile_text).
        - Any modification to resume content, skills, experience, or headline updates
          profile_text, automatically generating a new cache key and bypassing stale entries.
        - Reverse lookup mapping enables explicit invalidate(candidate_id) on resume activation.
        - Fail-safe: cache failures fall back cleanly to direct embedding computation.
    """

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._lock = threading.Lock()
        self._cache: OrderedDict[str, list[float]] = OrderedDict()
        self._candidate_keys: DefaultDict[str, set[str]] = defaultdict(set)
        self.hits: int = 0
        self.misses: int = 0

    def compute_key(
        self,
        candidate_id: UUID | str,
        profile_text: str,
        model_name: str = "",
    ) -> str:
        content = f"{str(candidate_id)}:{model_name}:{profile_text.strip()}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def get(
        self,
        candidate_id: UUID | str,
        profile_text: str,
        model_name: str = "",
    ) -> list[float] | None:
        key = self.compute_key(candidate_id, profile_text, model_name)
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self.hits += 1
                return list(self._cache[key])
            self.misses += 1
            return None

    def set(
        self,
        candidate_id: UUID | str,
        profile_text: str,
        embedding: list[float],
        model_name: str = "",
    ) -> None:
        key = self.compute_key(candidate_id, profile_text, model_name)
        cand_str = str(candidate_id)
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            else:
                while len(self._cache) >= self.max_size and self._cache:
                    oldest_key, _ = self._cache.popitem(last=False)
                    for c_id, keys in list(self._candidate_keys.items()):
                        keys.discard(oldest_key)
                        if not keys:
                            del self._candidate_keys[c_id]
                self._candidate_keys[cand_str].add(key)
            self._cache[key] = list(embedding)

    def invalidate(self, candidate_id: UUID | str) -> int:
        """Evict all cached embeddings for a specific candidate."""
        cand_str = str(candidate_id)
        count = 0
        with self._lock:
            keys = self._candidate_keys.pop(cand_str, set())
            for key in keys:
                if self._cache.pop(key, None) is not None:
                    count += 1
        return count

    def clear(self) -> None:
        """Clear the entire cache and reset metric counters."""
        with self._lock:
            self._cache.clear()
            self._candidate_keys.clear()
            self.hits = 0
            self.misses = 0


# Shared singleton cache instance for application-wide reuse
candidate_embedding_cache = CandidateEmbeddingCache(max_size=1000)


class CandidatePreparationInput(BaseModel):
    candidate_id: UUID
    resume_data: ResumeData


class CandidatePreparationResult(BaseModel):
    candidate_id: UUID
    representation: CandidateRepresentation
    embedding: list[float]


class CandidatePreparationService:
    def __init__(
        self,
        representation_builder: CandidateRepresentationBuilder,
        embedding_service: EmbeddingService,
        cache: CandidateEmbeddingCache | None = candidate_embedding_cache,
    ):
        self.representation_builder = representation_builder
        self.embedding_service = embedding_service
        self.cache = cache

    def prepare(
        self,
        data: CandidatePreparationInput,
    ) -> CandidatePreparationResult:
        representation = self.representation_builder.build(
            data.resume_data
        )

        embedding = None
        model_name = getattr(self.embedding_service, "model", "")

        if self.cache is not None:
            try:
                embedding = self.cache.get(
                    candidate_id=data.candidate_id,
                    profile_text=representation.profile_text,
                    model_name=model_name,
                )
            except Exception as exc:
                logger.warning("Candidate embedding cache get failed: %s", exc)
                embedding = None

        if embedding is None:
            embedding = self.embedding_service.embed_text(
                representation.profile_text
            )
            if self.cache is not None:
                try:
                    self.cache.set(
                        candidate_id=data.candidate_id,
                        profile_text=representation.profile_text,
                        embedding=embedding,
                        model_name=model_name,
                    )
                except Exception as exc:
                    logger.warning("Candidate embedding cache set failed: %s", exc)

        return CandidatePreparationResult(
            candidate_id=data.candidate_id,
            representation=representation,
            embedding=embedding,
        )


candidate_preparation_service = CandidatePreparationService(
    representation_builder=candidate_representation_builder,
    embedding_service=embedding_service,
    cache=candidate_embedding_cache,
)
