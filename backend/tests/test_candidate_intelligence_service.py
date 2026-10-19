from datetime import datetime, timezone
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.ai.candidate_intelligence.schemas import (
    CandidateIntelligenceFilterRequest,
    CandidateIntelligenceResponse,
)
from app.ai.candidate_intelligence.service import (
    CandidateIntelligenceService,
)
from app.ai.matching.explanation import MatchExplanation, MatchExplanationEvidence
from app.ai.matching.results import FinalMatchResult, RankedMatchResult
from app.models.application import Application, ApplicationStatus
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.resume import Resume


def make_ranked_match(*, rank: int, candidate_id: uuid4, overall_score: float) -> RankedMatchResult:
    return RankedMatchResult(
        rank=rank,
        candidate_id=candidate_id,
        overall_score=overall_score,
        required_skill_score=0.9,
        preferred_skill_score=0.8,
        semantic_similarity=0.85,
        required_matched=["Python", "FastAPI"],
        required_missing=[],
        preferred_matched=["Docker"],
        preferred_missing=["Kubernetes"],
    )


def make_final_match(*, rank: int, candidate_id: uuid4, overall_score: float) -> FinalMatchResult:
    match = make_ranked_match(rank=rank, candidate_id=candidate_id, overall_score=overall_score)
    explanation = MatchExplanation(
        summary="Candidate matches required backend qualifications.",
        strengths=["Strong Python mastery."],
        gaps=["Needs Kubernetes experience."],
        evidence=MatchExplanationEvidence(
            required_skill_score=0.9,
            preferred_skill_score=0.8,
            semantic_similarity=0.85,
        ),
        caveats=["Kubernetes is preferred."],
    )
    return FinalMatchResult(match=match, explanation=explanation)


def test_service_ownership_mismatch_raises_value_error():
    recruiter_a = Recruiter(id=uuid4(), user_id=uuid4())
    recruiter_b = Recruiter(id=uuid4(), user_id=uuid4())

    job = Job(id=uuid4(), recruiter_id=recruiter_b.id, title="Backend Dev", is_active=True)

    service = CandidateIntelligenceService()
    db_mock = MagicMock()

    with pytest.raises(ValueError, match="do not have permission"):
        service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter_a,
            job=job,
        )


def test_service_inactive_job_raises_value_error():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, title="Backend Dev", is_active=False)

    service = CandidateIntelligenceService()
    db_mock = MagicMock()

    with pytest.raises(ValueError, match="inactive"):
        service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter,
            job=job,
        )


def test_service_empty_candidates_returns_empty_response():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, title="Backend Dev", is_active=True)

    mock_matching_service = MagicMock()
    mock_matching_service.rank_and_explain_candidates.return_value = []
    mock_matching_service.rank_candidates.return_value = []

    service = CandidateIntelligenceService(matching_service=mock_matching_service)
    db_mock = MagicMock()

    response = service.get_candidate_intelligence(
        db=db_mock,
        recruiter=recruiter,
        job=job,
    )

    assert isinstance(response, CandidateIntelligenceResponse)
    assert response.total_candidates == 0
    assert response.matched_count == 0
    assert response.results == []


def test_service_orchestration_correlates_candidate_profile_and_application():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, title="Lead Python Engineer", is_active=True)

    cand1_id = uuid4()
    cand2_id = uuid4()

    cand1 = Candidate(
        id=cand1_id,
        user_id=uuid4(),
        first_name="Alice",
        last_name="Smith",
        headline="Senior Platform Engineer",
        location="Bengaluru",
        bio="Cloud infrastructure expert.",
    )

    cand2 = Candidate(
        id=cand2_id,
        user_id=uuid4(),
        first_name="Bob",
        last_name="Jones",
        headline="Backend Dev",
        location="Pune",
        bio="API builder.",
    )

    resume1 = Resume(
        id=uuid4(),
        candidate_id=cand1_id,
        is_active=True,
        parsing_status="COMPLETED",
        parsed_data={
            "headline": "Senior Platform Engineer",
            "skills": ["Python", "FastAPI", "Docker"],
            "experience": [
                {
                    "job_title": "Lead Dev",
                    "company": "CloudCorp",
                    "start_date": "2021",
                    "end_date": "Present",
                    "description": "Led backend engineering.",
                }
            ],
            "education": [
                {
                    "degree": "B.Tech",
                    "institution": "IIT Bombay",
                }
            ],
        },
    )

    app1 = Application(
        id=uuid4(),
        candidate_id=cand1_id,
        job_id=job.id,
        status=ApplicationStatus.APPLIED,
        created_at=datetime.now(timezone.utc),
    )

    mock_matching_service = MagicMock()
    mock_matching_service.rank_and_explain_candidates.return_value = [
        make_final_match(rank=1, candidate_id=cand1_id, overall_score=0.92),
        make_final_match(rank=2, candidate_id=cand2_id, overall_score=0.74),
    ]

    service = CandidateIntelligenceService(matching_service=mock_matching_service)

    db_mock = MagicMock()
    # Mock Candidate queries
    cand_query_mock = MagicMock()
    cand_query_mock.filter.return_value.all.return_value = [cand1, cand2]

    # Mock Application queries
    app_query_mock = MagicMock()
    app_query_mock.filter.return_value.all.return_value = [app1]

    def query_side_effect(model):
        if model == Candidate:
            return cand_query_mock
        if model == Application:
            return app_query_mock
        return MagicMock()

    db_mock.query.side_effect = query_side_effect

    # Mock get_active_resume and get_candidate_skills
    with (
        pytest.MonkeyPatch.context() as mp,
    ):
        mp.setattr(
            "app.ai.candidate_intelligence.service.get_active_resume",
            lambda db, candidate: resume1 if candidate.id == cand1_id else None,
        )
        mp.setattr(
            "app.ai.candidate_intelligence.service.get_candidate_skills",
            lambda db, candidate: [],
        )

        response = service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter,
            job=job,
            filters=CandidateIntelligenceFilterRequest(include_explanations=True),
        )

    assert response.job_id == job.id
    assert response.total_candidates == 2
    assert response.matched_count == 2
    assert len(response.results) == 2

    first_item = response.results[0]
    assert first_item.candidate.full_name == "Alice Smith"
    assert first_item.candidate.headline == "Senior Platform Engineer"
    assert len(first_item.candidate.experience) == 1
    assert first_item.candidate.experience[0].company == "CloudCorp"
    assert first_item.application is not None
    assert first_item.application.status == "applied"
    assert first_item.explanation is not None

    second_item = response.results[1]
    assert second_item.candidate.full_name == "Bob Jones"
    assert second_item.application is None  # Candidate 2 did not apply


def test_service_query_filtering():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, title="Backend Dev", is_active=True)

    cand1_id = uuid4()
    cand2_id = uuid4()

    cand1 = Candidate(id=cand1_id, user_id=uuid4(), first_name="Kavita", last_name="Sharma", headline="Python Architect")
    cand2 = Candidate(id=cand2_id, user_id=uuid4(), first_name="Rahul", last_name="Verma", headline="Java Developer")

    mock_matching_service = MagicMock()
    mock_matching_service.rank_and_explain_candidates.return_value = [
        make_final_match(rank=1, candidate_id=cand1_id, overall_score=0.9),
        make_final_match(rank=2, candidate_id=cand2_id, overall_score=0.7),
    ]

    service = CandidateIntelligenceService(matching_service=mock_matching_service)
    db_mock = MagicMock()

    cand_query_mock = MagicMock()
    cand_query_mock.filter.return_value.all.return_value = [cand1, cand2]
    app_query_mock = MagicMock()
    app_query_mock.filter.return_value.all.return_value = []

    db_mock.query.side_effect = lambda m: cand_query_mock if m == Candidate else app_query_mock

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.candidate_intelligence.service.get_active_resume", lambda db, candidate: None)
        mp.setattr("app.ai.candidate_intelligence.service.get_candidate_skills", lambda db, candidate: [])

        # Filter by name "kavita"
        res1 = service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter,
            job=job,
            filters=CandidateIntelligenceFilterRequest(query="Kavita"),
        )
        assert res1.matched_count == 1
        assert res1.results[0].candidate.full_name == "Kavita Sharma"

        # Filter by headline "Java"
        res2 = service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter,
            job=job,
            filters=CandidateIntelligenceFilterRequest(query="Java"),
        )
        assert res2.matched_count == 1
        assert res2.results[0].candidate.full_name == "Rahul Verma"


def test_service_min_score_and_application_status_filtering():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, title="Backend Dev", is_active=True)

    cand1_id = uuid4()
    cand2_id = uuid4()

    cand1 = Candidate(id=cand1_id, user_id=uuid4(), first_name="Alice", last_name="A")
    cand2 = Candidate(id=cand2_id, user_id=uuid4(), first_name="Bob", last_name="B")

    app1 = Application(id=uuid4(), candidate_id=cand1_id, job_id=job.id, status=ApplicationStatus.APPLIED)

    mock_matching_service = MagicMock()
    mock_matching_service.rank_and_explain_candidates.return_value = [
        make_final_match(rank=1, candidate_id=cand1_id, overall_score=0.88),
        make_final_match(rank=2, candidate_id=cand2_id, overall_score=0.55),
    ]

    service = CandidateIntelligenceService(matching_service=mock_matching_service)
    db_mock = MagicMock()

    cand_query_mock = MagicMock()
    cand_query_mock.filter.return_value.all.return_value = [cand1, cand2]
    app_query_mock = MagicMock()
    app_query_mock.filter.return_value.all.return_value = [app1]

    db_mock.query.side_effect = lambda m: cand_query_mock if m == Candidate else app_query_mock

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.candidate_intelligence.service.get_active_resume", lambda db, candidate: None)
        mp.setattr("app.ai.candidate_intelligence.service.get_candidate_skills", lambda db, candidate: [])

        # Filter by min_score 0.80 -> only Alice
        res_score = service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter,
            job=job,
            filters=CandidateIntelligenceFilterRequest(min_score=0.80),
        )
        assert res_score.matched_count == 1
        assert res_score.results[0].candidate.full_name == "Alice A"

        # Filter by application_status "not_applied" -> only Bob
        res_status = service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter,
            job=job,
            filters=CandidateIntelligenceFilterRequest(application_status="not_applied"),
        )
        assert res_status.matched_count == 1
        assert res_status.results[0].candidate.full_name == "Bob B"


def test_service_does_not_mutate_database():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, title="Backend Dev", is_active=True)

    mock_matching_service = MagicMock()
    mock_matching_service.rank_candidates.return_value = []

    service = CandidateIntelligenceService(matching_service=mock_matching_service)
    db_mock = MagicMock()

    service.get_candidate_intelligence(
        db=db_mock,
        recruiter=recruiter,
        job=job,
        filters=CandidateIntelligenceFilterRequest(include_explanations=False),
    )

    db_mock.commit.assert_not_called()
    db_mock.add.assert_not_called()
    db_mock.flush.assert_not_called()


def test_service_sorting_options():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, title="Backend Dev", is_active=True)

    c1_id = uuid4()
    c2_id = uuid4()

    cand1 = Candidate(id=c1_id, user_id=uuid4(), first_name="Zara", last_name="Khan")
    cand2 = Candidate(id=c2_id, user_id=uuid4(), first_name="Aarav", last_name="Patel")

    mock_matching_service = MagicMock()
    mock_matching_service.rank_candidates.return_value = [
        make_ranked_match(rank=1, candidate_id=c1_id, overall_score=0.92),
        make_ranked_match(rank=2, candidate_id=c2_id, overall_score=0.74),
    ]

    service = CandidateIntelligenceService(matching_service=mock_matching_service)
    db_mock = MagicMock()

    cand_query_mock = MagicMock()
    cand_query_mock.filter.return_value.all.return_value = [cand1, cand2]
    app_query_mock = MagicMock()
    app_query_mock.filter.return_value.all.return_value = []

    db_mock.query.side_effect = lambda m: cand_query_mock if m == Candidate else app_query_mock

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.candidate_intelligence.service.get_active_resume", lambda db, candidate: None)
        mp.setattr("app.ai.candidate_intelligence.service.get_candidate_skills", lambda db, candidate: [])

        # Sort by rank asc -> rank 1 (Zara), then rank 2 (Aarav)
        res_rank_asc = service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter,
            job=job,
            filters=CandidateIntelligenceFilterRequest(
                include_explanations=False,
                sort_by="rank",
                sort_order="asc",
            ),
        )
        assert [r.rank for r in res_rank_asc.results] == [1, 2]

        # Sort by rank desc -> rank 2 (Aarav), then rank 1 (Zara)
        res_rank_desc = service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter,
            job=job,
            filters=CandidateIntelligenceFilterRequest(
                include_explanations=False,
                sort_by="rank",
                sort_order="desc",
            ),
        )
        assert [r.rank for r in res_rank_desc.results] == [2, 1]

        # Sort by name asc -> Aarav Patel, then Zara Khan
        res_name_asc = service.get_candidate_intelligence(
            db=db_mock,
            recruiter=recruiter,
            job=job,
            filters=CandidateIntelligenceFilterRequest(
                include_explanations=False,
                sort_by="name",
                sort_order="asc",
            ),
        )
        assert res_name_asc.results[0].candidate.full_name == "Aarav Patel"
        assert res_name_asc.results[1].candidate.full_name == "Zara Khan"
