from uuid import UUID

from app.ai.parsers.schemas import ResumeData
from app.ai.representations.candidate import CandidateRepresentation
from app.ai.services.candidate_preparation_service import (
    CandidateEmbeddingCache,
    CandidatePreparationInput,
    CandidatePreparationService,
    candidate_embedding_cache,
)


class FakeRepresentationBuilder:
    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def build(self, resume_data):
        skills_str = ", ".join(resume_data.skills) if resume_data.skills else "None"
        headline = f"\nHeadline:\n{resume_data.headline}" if resume_data.headline else ""
        return CandidateRepresentation(
            profile_text=f"Candidate Profile{self.prefix}\n\nSkills:\n{skills_str}{headline}"
        )


class FakeEmbeddingService:
    def __init__(self, model_name: str = "fake-embedding-model"):
        self.received_text = None
        self.call_count = 0
        self.model = model_name

    def embed_text(self, text):
        self.received_text = text
        self.call_count += 1
        return [0.1, 0.2, 0.3]


def test_candidate_preparation_service_builds_representation_and_embedding():
    candidate_embedding_cache.clear()
    candidate_id = UUID("11111111-1111-1111-1111-111111111111")

    resume_data = ResumeData(
        name="Test Candidate",
        skills=["Python"],
    )

    service = CandidatePreparationService(
        representation_builder=FakeRepresentationBuilder(),
        embedding_service=FakeEmbeddingService(),
        cache=None,
    )

    data = CandidatePreparationInput(
        candidate_id=candidate_id,
        resume_data=resume_data,
    )

    result = service.prepare(data)

    assert result.candidate_id == candidate_id
    assert "Skills:\nPython" in result.representation.profile_text
    assert result.embedding == [0.1, 0.2, 0.3]


def test_candidate_preparation_service_passes_representation_text_to_embedding():
    candidate_embedding_cache.clear()
    candidate_id = UUID("11111111-1111-1111-1111-111111111111")

    resume_data = ResumeData(
        name="Test Candidate",
        skills=["Python"],
    )

    fake_embedding_service = FakeEmbeddingService()

    service = CandidatePreparationService(
        representation_builder=FakeRepresentationBuilder(),
        embedding_service=fake_embedding_service,
        cache=None,
    )

    data = CandidatePreparationInput(
        candidate_id=candidate_id,
        resume_data=resume_data,
    )

    service.prepare(data)

    assert fake_embedding_service.received_text == (
        "Candidate Profile\n\nSkills:\nPython"
    )
    assert fake_embedding_service.call_count == 1


def test_candidate_embedding_cache_avoids_duplicate_calls_for_unchanged_profile():
    test_cache = CandidateEmbeddingCache(max_size=10)
    fake_embedding_service = FakeEmbeddingService()

    service = CandidatePreparationService(
        representation_builder=FakeRepresentationBuilder(),
        embedding_service=fake_embedding_service,
        cache=test_cache,
    )

    candidate_id = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    resume_data = ResumeData(name="Candidate A", skills=["Python", "FastAPI"])
    data = CandidatePreparationInput(candidate_id=candidate_id, resume_data=resume_data)

    # First call: cache miss, invokes embed_text
    res1 = service.prepare(data)
    assert fake_embedding_service.call_count == 1
    assert test_cache.misses == 1
    assert test_cache.hits == 0
    assert res1.embedding == [0.1, 0.2, 0.3]

    # Second call with unchanged profile: cache hit, zero new calls to embed_text
    res2 = service.prepare(data)
    assert fake_embedding_service.call_count == 1  # Unchanged!
    assert test_cache.hits == 1
    assert res2.embedding == [0.1, 0.2, 0.3]


def test_candidate_embedding_cache_recomputes_when_profile_changes():
    test_cache = CandidateEmbeddingCache(max_size=10)
    fake_embedding_service = FakeEmbeddingService()

    service = CandidatePreparationService(
        representation_builder=FakeRepresentationBuilder(),
        embedding_service=fake_embedding_service,
        cache=test_cache,
    )

    candidate_id = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
    initial_resume = ResumeData(name="Candidate B", skills=["Python"])
    data1 = CandidatePreparationInput(candidate_id=candidate_id, resume_data=initial_resume)

    service.prepare(data1)
    assert fake_embedding_service.call_count == 1

    # Candidate profile changes (new skill added)
    updated_resume = ResumeData(name="Candidate B", skills=["Python", "PostgreSQL"])
    data2 = CandidatePreparationInput(candidate_id=candidate_id, resume_data=updated_resume)

    service.prepare(data2)
    # Content-addressable key changed -> recomputed!
    assert fake_embedding_service.call_count == 2
    assert "PostgreSQL" in fake_embedding_service.received_text


def test_different_candidates_do_not_share_cache():
    test_cache = CandidateEmbeddingCache(max_size=10)
    fake_embedding_service = FakeEmbeddingService()

    service = CandidatePreparationService(
        representation_builder=FakeRepresentationBuilder(),
        embedding_service=fake_embedding_service,
        cache=test_cache,
    )

    c1_id = UUID("11111111-1111-1111-1111-111111111111")
    c2_id = UUID("22222222-2222-2222-2222-222222222222")

    resume_data = ResumeData(name="Identical Content", skills=["Python"])
    data_c1 = CandidatePreparationInput(candidate_id=c1_id, resume_data=resume_data)
    data_c2 = CandidatePreparationInput(candidate_id=c2_id, resume_data=resume_data)

    service.prepare(data_c1)
    assert fake_embedding_service.call_count == 1

    service.prepare(data_c2)
    # Different candidate_id must compute separate key and invoke embed_text
    assert fake_embedding_service.call_count == 2


def test_candidate_embedding_cache_explicit_invalidation():
    test_cache = CandidateEmbeddingCache(max_size=10)
    fake_embedding_service = FakeEmbeddingService()

    service = CandidatePreparationService(
        representation_builder=FakeRepresentationBuilder(),
        embedding_service=fake_embedding_service,
        cache=test_cache,
    )

    candidate_id = UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")
    resume_data = ResumeData(name="Candidate C", skills=["Python"])
    data = CandidatePreparationInput(candidate_id=candidate_id, resume_data=resume_data)

    service.prepare(data)
    assert fake_embedding_service.call_count == 1

    # Invalidate candidate explicitly
    invalidated = test_cache.invalidate(candidate_id)
    assert invalidated == 1

    # Next call forces recomputation
    service.prepare(data)
    assert fake_embedding_service.call_count == 2


def test_candidate_embedding_cache_safe_fallback_on_error():
    class BrokenCache:
        def get(self, *args, **kwargs):
            raise RuntimeError("Cache storage hardware failure")
        def set(self, *args, **kwargs):
            raise RuntimeError("Cache write error")

    fake_embedding_service = FakeEmbeddingService()
    service = CandidatePreparationService(
        representation_builder=FakeRepresentationBuilder(),
        embedding_service=fake_embedding_service,
        cache=BrokenCache(),  # type: ignore
    )

    candidate_id = UUID("dddddddd-dddd-dddd-dddd-dddddddddddd")
    resume_data = ResumeData(name="Candidate D", skills=["Python"])
    data = CandidatePreparationInput(candidate_id=candidate_id, resume_data=resume_data)

    # Must not raise RuntimeError, must fall back to direct embed_text computation
    result = service.prepare(data)
    assert result.embedding == [0.1, 0.2, 0.3]
    assert fake_embedding_service.call_count == 1
