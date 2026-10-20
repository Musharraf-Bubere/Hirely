import pytest

from app.ai.services.candidate_preparation_service import candidate_embedding_cache
from app.core.rate_limit import ai_rate_limiter, auth_rate_limiter


@pytest.fixture(autouse=True)
def reset_in_memory_state():
    """
    Ensure in-memory state (rate limiters and candidate embedding cache)
    is isolated and clean across every test case.
    """
    candidate_embedding_cache.clear()
    ai_rate_limiter.reset()
    auth_rate_limiter.reset()
    yield
    candidate_embedding_cache.clear()
    ai_rate_limiter.reset()
    auth_rate_limiter.reset()
