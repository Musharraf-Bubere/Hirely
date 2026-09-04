import pytest

from app.ai.matching.skill_matching import SkillMatcher


def test_skill_matching():
    matcher = SkillMatcher()

    result = matcher.match(
        candidate_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
        ],
        required_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
        ],
        preferred_skills=[
            "Docker",
            "AWS",
        ],
    )

    assert result.required_score == pytest.approx(1.0)
    assert result.preferred_score == pytest.approx(0.5)

    assert result.required_matched == [
        "Python",
        "FastAPI",
        "PostgreSQL",
    ]

    assert result.required_missing == []

    assert result.preferred_matched == ["Docker"]
    assert result.preferred_missing == ["AWS"]


def test_skill_matching_is_case_insensitive_and_trimmed():
    matcher = SkillMatcher()

    result = matcher.match(
        candidate_skills=[
            " Python ",
            "FASTAPI",
            " postgresql",
        ],
        required_skills=[
            "python",
            "FastAPI",
            "PostgreSQL",
        ],
        preferred_skills=[],
    )

    assert result.required_score == pytest.approx(1.0)

    assert result.required_matched == [
        "python",
        "FastAPI",
        "PostgreSQL",
    ]

    assert result.required_missing == []


def test_missing_required_and_preferred_skills():
    matcher = SkillMatcher()

    result = matcher.match(
        candidate_skills=[
            "Python",
            "Docker",
        ],
        required_skills=[
            "Python",
            "FastAPI",
            "PostgreSQL",
        ],
        preferred_skills=[
            "Docker",
            "AWS",
        ],
    )

    assert result.required_score == pytest.approx(1 / 3)
    assert result.preferred_score == pytest.approx(1 / 2)

    assert result.required_matched == ["Python"]

    assert result.required_missing == [
        "FastAPI",
        "PostgreSQL",
    ]

    assert result.preferred_matched == ["Docker"]
    assert result.preferred_missing == ["AWS"]


def test_empty_skill_requirements():
    matcher = SkillMatcher()

    result = matcher.match(
        candidate_skills=["Python"],
        required_skills=[],
        preferred_skills=[],
    )

    assert result.required_score == pytest.approx(1.0)
    assert result.preferred_score == pytest.approx(1.0)

    assert result.required_matched == []
    assert result.required_missing == []
    assert result.preferred_matched == []
    assert result.preferred_missing == []