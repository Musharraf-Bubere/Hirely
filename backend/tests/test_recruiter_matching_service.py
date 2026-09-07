from uuid import uuid4

from app.ai.matching.results import (
    CompleteMatchResult,
    MatchScoreResult,
    RankedMatchResult,
    SkillMatchResult,
)
from app.ai.representations.candidate import CandidateRepresentation
from app.ai.representations.job import JobRepresentation
from app.ai.services.candidate_preparation_service import (
    CandidatePreparationResult,
)
from app.ai.services.job_preparation_service import (
    JobPreparationResult,
)
from app.ai.services.recruiter_matching_service import (
    RecruiterMatchingService,
)
from app.models.job import Job


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def create_mock_job():
    return Job(
        id=uuid4(),
        recruiter_id=uuid4(),
        title="Python Backend Developer",
        description="Build backend APIs using Python and FastAPI.",
        location="Mumbai",
        employment_type="FULL_TIME",
        experience_level="MID",
        is_active=True,
    )


def create_ranked_match(
    candidate_id=None,
    rank=1,
    overall_score=0.90,
):
    candidate_id = candidate_id or uuid4()

    return RankedMatchResult(
        rank=rank,
        candidate_id=candidate_id,
        overall_score=overall_score,
        required_skill_score=1.0,
        preferred_skill_score=0.8,
        semantic_similarity=0.9,
        required_matched=["Python"],
        required_missing=[],
        preferred_matched=["FastAPI"],
        preferred_missing=[],
    )


# ---------------------------------------------------------
# Mock Dependencies
# ---------------------------------------------------------

class FakeJobPreparationService:

    def __init__(self):
        self.calls = []

    def prepare(self, data):
        self.calls.append(data)

        representation = JobRepresentation(
            job_id=data.job_id,
            title=data.title,
            description=data.description,
            location=data.location,
            employment_type=data.employment_type,
            experience_level=data.experience_level,
            required_skills=data.required_skills,
            preferred_skills=data.preferred_skills,
            job_text="mock job",
        )

        return JobPreparationResult(
            job_id=data.job_id,
            representation=representation,
            embedding=[0.1, 0.2, 0.3],
        )


class FakeCandidatePreparationService:

    def __init__(self):
        self.calls = []

    def prepare(self, data):
        self.calls.append(data)

        representation = CandidateRepresentation(
            candidate_id=data.candidate_id,
            profile_text="mock candidate",
        )

        return CandidatePreparationResult(
            candidate_id=data.candidate_id,
            representation=representation,
            embedding=[0.1, 0.2, 0.3],
        )


class FakeMatchingInputAssembler:

    def __init__(self):
        self.calls = []

    def assemble(self, data):
        self.calls.append(data)

        return type(
            "FakeMatchingInput",
            (),
            {
                "candidate_id": (
                    data.candidate_preparation.candidate_id
                ),
                "candidate_skills": data.candidate_skills,
                "required_skills": data.required_skills,
                "preferred_skills": data.preferred_skills,
                "candidate_embedding": (
                    data.candidate_preparation.embedding
                ),
                "job_embedding": (
                    data.job_preparation.embedding
                ),
            },
        )()


class FakeMatchingOrchestrator:

    def __init__(self):
        self.match_calls = []
        self.rank_calls = []
        self.explanation_calls = []

    def match(self, matching_input):
        self.match_calls.append(matching_input)

        score = MatchScoreResult(
            candidate_id=matching_input.candidate_id,
            overall_score=0.90,
            required_skill_score=1.0,
            preferred_skill_score=0.8,
            semantic_similarity=0.9,
        )

        skills = SkillMatchResult(
            required_score=1.0,
            preferred_score=0.8,
            required_matched=["Python"],
            required_missing=[],
            preferred_matched=["FastAPI"],
            preferred_missing=[],
        )

        return CompleteMatchResult(
            score=score,
            skills=skills,
        )

    def rank_match_results(self, matching_results):
        self.rank_calls.append(matching_results)

        return [
            create_ranked_match(
                candidate_id=result.score.candidate_id,
                rank=index,
                overall_score=result.score.overall_score,
            )
            for index, result in enumerate(
                matching_results,
                start=1,
            )
        ]

    def explain_ranked_matches(self, explanation_request):
        self.explanation_calls.append(
            explanation_request
        )

        results = []

        selected_ids = {
            match.candidate_id
            for match in explanation_request.ranked_matches[
                : explanation_request.explanation_limit
            ]
        }

        for match in explanation_request.ranked_matches:

            if match.candidate_id in selected_ids:
                explanation = type(
                    "FakeExplanation",
                    (),
                    {
                        "summary": "Mock explanation",
                        "strengths": ["Python"],
                        "gaps": [],
                        "evidence": {},
                        "caveats": [],
                    },
                )()
            else:
                explanation = None

            results.append(
                type(
                    "FakeFinalMatchResult",
                    (),
                    {
                        "match": match,
                        "explanation": explanation,
                    },
                )()
            )

        return results


# ---------------------------------------------------------
# Service Factory
# ---------------------------------------------------------

def create_service():

    candidate_preparation_service = (
        FakeCandidatePreparationService()
    )

    job_preparation_service = (
        FakeJobPreparationService()
    )

    matching_input_assembler = (
        FakeMatchingInputAssembler()
    )

    matching_orchestrator = (
        FakeMatchingOrchestrator()
    )

    service = RecruiterMatchingService(
        candidate_preparation_service=(
            candidate_preparation_service
        ),
        job_preparation_service=(
            job_preparation_service
        ),
        matching_input_assembler=(
            matching_input_assembler
        ),
        matching_orchestrator=(
            matching_orchestrator
        ),
    )

    return (
        service,
        candidate_preparation_service,
        job_preparation_service,
        matching_input_assembler,
        matching_orchestrator,
    )


# ---------------------------------------------------------
# 1. Job preparation
# ---------------------------------------------------------

def test_recruiter_matching_service_prepares_job_once(
    monkeypatch,
):
    service, _, job_service, _, _ = create_service()

    job = create_mock_job()

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_job_skills",
        lambda db, job: (
            ["Python"],
            ["FastAPI"],
        ),
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_candidates",
        lambda db: [],
    )

    results = service.rank_candidates(
        db=None,
        job=job,
    )

    assert results == []

    assert len(job_service.calls) == 1

    assert job_service.calls[0].job_id == job.id
    assert job_service.calls[0].required_skills == ["Python"]
    assert job_service.calls[0].preferred_skills == ["FastAPI"]


# ---------------------------------------------------------
# 2. Candidate eligibility
# ---------------------------------------------------------

def test_recruiter_matching_service_skips_candidates_without_resume(
    monkeypatch,
):
    service, _, _, _, orchestrator = create_service()

    job = create_mock_job()

    candidate = type(
        "FakeCandidate",
        (),
        {
            "id": uuid4(),
        },
    )()

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_job_skills",
        lambda db, job: (
            ["Python"],
            [],
        ),
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_candidates",
        lambda db: [candidate],
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_active_resume",
        lambda db, candidate: None,
    )

    results = service.rank_candidates(
        db=None,
        job=job,
    )

    assert results == []
    assert orchestrator.match_calls == []


# ---------------------------------------------------------
# 3. Pending resume is skipped
# ---------------------------------------------------------

def test_recruiter_matching_service_skips_pending_resume(
    monkeypatch,
):
    service, _, _, _, orchestrator = create_service()

    job = create_mock_job()

    candidate = type(
        "FakeCandidate",
        (),
        {
            "id": uuid4(),
        },
    )()

    resume = type(
        "FakeResume",
        (),
        {
            "parsing_status": "PENDING",
            "parsed_data": None,
        },
    )()

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_job_skills",
        lambda db, job: (
            ["Python"],
            [],
        ),
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_candidates",
        lambda db: [candidate],
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_active_resume",
        lambda db, candidate: resume,
    )

    results = service.rank_candidates(
        db=None,
        job=job,
    )

    assert results == []
    assert orchestrator.match_calls == []


# ---------------------------------------------------------
# 4. Candidate with completed resume is matched
# ---------------------------------------------------------

def test_recruiter_matching_service_matches_eligible_candidate(
    monkeypatch,
):
    (
        service,
        candidate_service,
        _,
        assembler,
        orchestrator,
    ) = create_service()

    job = create_mock_job()

    candidate = type(
        "FakeCandidate",
        (),
        {
            "id": uuid4(),
        },
    )()

    resume = type(
        "FakeResume",
        (),
        {
            "parsing_status": "COMPLETED",
            "parsed_data": {
                "name": "Test Candidate",
                "skills": ["Python"],
            },
        },
    )()

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_job_skills",
        lambda db, job: (
            ["Python"],
            ["FastAPI"],
        ),
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_candidates",
        lambda db: [candidate],
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_active_resume",
        lambda db, candidate: resume,
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_candidate_skills",
        lambda db, candidate: ["Python"],
    )

    results = service.rank_candidates(
        db=None,
        job=job,
    )

    assert len(results) == 1
    assert results[0].candidate_id == candidate.id
    assert results[0].rank == 1

    assert len(candidate_service.calls) == 1
    assert len(assembler.calls) == 1
    assert len(orchestrator.match_calls) == 1
    assert len(orchestrator.rank_calls) == 1


# ---------------------------------------------------------
# 5. Multiple candidates are ranked
# ---------------------------------------------------------

def test_recruiter_matching_service_ranks_multiple_candidates(
    monkeypatch,
):
    service, _, _, _, orchestrator = create_service()

    job = create_mock_job()

    candidate_1 = type(
        "FakeCandidate",
        (),
        {
            "id": uuid4(),
        },
    )()

    candidate_2 = type(
        "FakeCandidate",
        (),
        {
            "id": uuid4(),
        },
    )()

    resume = type(
        "FakeResume",
        (),
        {
            "parsing_status": "COMPLETED",
            "parsed_data": {
                "name": "Test Candidate",
                "skills": ["Python"],
            },
        },
    )()

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_job_skills",
        lambda db, job: (
            ["Python"],
            [],
        ),
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_candidates",
        lambda db: [
            candidate_1,
            candidate_2,
        ],
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_active_resume",
        lambda db, candidate: resume,
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_candidate_skills",
        lambda db, candidate: ["Python"],
    )

    results = service.rank_candidates(
        db=None,
        job=job,
    )

    assert len(results) == 2
    assert results[0].rank == 1
    assert results[1].rank == 2

    assert len(orchestrator.match_calls) == 2
    assert len(orchestrator.rank_calls) == 1


# ---------------------------------------------------------
# 6. Top-N explanations
# ---------------------------------------------------------

def test_recruiter_matching_service_explains_only_top_n():
    service, _, _, _, orchestrator = create_service()

    candidate_1 = uuid4()
    candidate_2 = uuid4()
    candidate_3 = uuid4()

    ranked_results = [
        create_ranked_match(
            candidate_id=candidate_1,
            rank=1,
            overall_score=0.95,
        ),
        create_ranked_match(
            candidate_id=candidate_2,
            rank=2,
            overall_score=0.90,
        ),
        create_ranked_match(
            candidate_id=candidate_3,
            rank=3,
            overall_score=0.80,
        ),
    ]

    results = service.explain_ranked_candidates(
        ranked_results=ranked_results,
        explanation_limit=2,
    )

    assert len(results) == 3

    assert results[0].explanation is not None
    assert results[1].explanation is not None
    assert results[2].explanation is None

    assert len(orchestrator.explanation_calls) == 1

    request = orchestrator.explanation_calls[0]

    assert request.explanation_limit == 2
    assert len(request.ranked_matches) == 3


# ---------------------------------------------------------
# 7. Rank + explain workflow
# ---------------------------------------------------------

def test_recruiter_matching_service_rank_and_explain(
    monkeypatch,
):
    service, _, _, _, orchestrator = create_service()

    job = create_mock_job()

    candidate = type(
        "FakeCandidate",
        (),
        {
            "id": uuid4(),
        },
    )()

    resume = type(
        "FakeResume",
        (),
        {
            "parsing_status": "COMPLETED",
            "parsed_data": {
                "name": "Test Candidate",
                "skills": ["Python"],
            },
        },
    )()

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_job_skills",
        lambda db, job: (
            ["Python"],
            [],
        ),
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_candidates",
        lambda db: [candidate],
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_active_resume",
        lambda db, candidate: resume,
    )

    monkeypatch.setattr(
        "app.ai.services.recruiter_matching_service.get_candidate_skills",
        lambda db, candidate: ["Python"],
    )

    results = service.rank_and_explain_candidates(
        db=None,
        job=job,
        explanation_limit=1,
    )

    assert len(results) == 1
    assert results[0].match.candidate_id == candidate.id
    assert results[0].explanation is not None

    assert len(orchestrator.match_calls) == 1
    assert len(orchestrator.rank_calls) == 1
    assert len(orchestrator.explanation_calls) == 1