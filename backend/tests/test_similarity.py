import pytest

from app.ai.matching.similarity import cosine_similarity


def test_identical_vectors_have_similarity_one():
    vector = [1.0, 2.0, 3.0]

    result = cosine_similarity(vector, vector)

    assert result == pytest.approx(1.0)


def test_orthogonal_vectors_have_similarity_zero():
    vector_a = [1.0, 0.0]
    vector_b = [0.0, 1.0]

    result = cosine_similarity(vector_a, vector_b)

    assert result == pytest.approx(0.0)


def test_opposite_vectors_have_similarity_negative_one():
    vector_a = [1.0, 0.0]
    vector_b = [-1.0, 0.0]

    result = cosine_similarity(vector_a, vector_b)

    assert result == pytest.approx(-1.0)


def test_different_dimensions_are_rejected():
    vector_a = [1.0, 2.0, 3.0]
    vector_b = [1.0, 2.0]

    with pytest.raises(
        ValueError,
        match="Vectors must have the same dimensions",
    ):
        cosine_similarity(vector_a, vector_b)


def test_zero_magnitude_vector_is_rejected():
    vector_a = [0.0, 0.0]
    vector_b = [1.0, 2.0]

    with pytest.raises(
        ValueError,
        match="Vectors cannot have zero magnitude",
    ):
        cosine_similarity(vector_a, vector_b)


def test_empty_vectors_are_rejected():
    with pytest.raises(
        ValueError,
        match="Vectors cannot be empty",
    ):
        cosine_similarity([], [])