from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.ai.parsers.schemas import ResumeData, WorkExperience
from app.ai.rag.schemas import (
    CandidateEvidenceAIResult,
    CandidateEvidenceQueryRequest,
    EvidenceCitation,
    EvidenceChunk,
    EvidenceConfidence,
)
from app.ai.rag.service import CandidateEvidenceRAGService
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.models.resume import Resume


def test_rag_service_ownership_mismatch():
    recruiter_a = Recruiter(id=uuid4(), user_id=uuid4())
    recruiter_b = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter_b.id, is_active=True, title="Backend Dev")

    service = CandidateEvidenceRAGService()
    db = MagicMock()

    with pytest.raises(ValueError, match="permission"):
        service.ask_candidate_evidence(
            db=db,
            recruiter=recruiter_a,
            job=job,
            candidate_id=uuid4(),
            request=CandidateEvidenceQueryRequest(query="Kafka experience"),
        )


def test_rag_service_inactive_job():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=False, title="Backend Dev")

    service = CandidateEvidenceRAGService()
    db = MagicMock()

    with pytest.raises(ValueError, match="inactive"):
        service.ask_candidate_evidence(
            db=db,
            recruiter=recruiter,
            job=job,
            candidate_id=uuid4(),
            request=CandidateEvidenceQueryRequest(query="Kafka experience"),
        )


def test_rag_service_missing_candidate():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=True, title="Backend Dev")

    service = CandidateEvidenceRAGService()
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError, match="Candidate not found"):
        service.ask_candidate_evidence(
            db=db,
            recruiter=recruiter,
            job=job,
            candidate_id=uuid4(),
            request=CandidateEvidenceQueryRequest(query="Kafka experience"),
        )


def test_rag_service_missing_active_resume():
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=True, title="Backend Dev")
    candidate = Candidate(id=uuid4(), user_id=uuid4(), first_name="Aarav", last_name="Sharma")

    service = CandidateEvidenceRAGService()
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = candidate

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.rag.service.get_active_resume", lambda db, candidate: None)

        with pytest.raises(ValueError, match="active resume"):
            service.ask_candidate_evidence(
                db=db,
                recruiter=recruiter,
                job=job,
                candidate_id=candidate.id,
                request=CandidateEvidenceQueryRequest(query="Kafka experience"),
            )


def test_rag_service_unrelated_query_no_chunks_retrieved_skips_ai():
    """When retriever finds 0 chunks above threshold, return insufficient evidence without calling Gemini."""
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=True, title="Backend Dev")
    candidate = Candidate(id=uuid4(), user_id=uuid4(), first_name="Aarav", last_name="Sharma")

    resume_data = ResumeData(
        experience=[
            WorkExperience(
                company="TechCorp",
                job_title="Developer",
                description="Built web applications with Django and Python.",
            )
        ]
    )
    resume = Resume(
        id=uuid4(),
        candidate_id=candidate.id,
        parsing_status="COMPLETED",
        parsed_data=resume_data.model_dump(),
        is_active=True,
    )

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = candidate

    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = []  # No chunks above threshold

    mock_ai = MagicMock()

    service = CandidateEvidenceRAGService(
        retriever=mock_retriever,
        ai_service=mock_ai,
    )

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.rag.service.get_active_resume", lambda db, candidate: resume)

        response = service.ask_candidate_evidence(
            db=db,
            recruiter=recruiter,
            job=job,
            candidate_id=candidate.id,
            request=CandidateEvidenceQueryRequest(query="Aerospace rocketry propulsion"),
        )

        assert response.has_evidence is False
        assert response.confidence == "none"
        assert response.citations == []
        assert response.retrieved_chunk_count == 0
        assert "No direct evidence" in response.answer

        # Verify Gemini was NOT called
        mock_ai.generate_structured.assert_not_called()


def test_rag_service_rejects_invalid_citation_source_ids():
    """Citations referencing chunks not in the retrieved set are discarded."""
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=True, title="Backend Dev")
    candidate = Candidate(id=uuid4(), user_id=uuid4(), first_name="Aarav", last_name="Sharma")

    resume_data = ResumeData(
        experience=[
            WorkExperience(
                company="DataStream",
                job_title="Streaming Engineer",
                description="Built real-time Kafka consumers with 10k messages per second.",
            )
        ]
    )
    resume = Resume(
        id=uuid4(),
        candidate_id=candidate.id,
        parsing_status="COMPLETED",
        parsed_data=resume_data.model_dump(),
        is_active=True,
    )

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = candidate

    # Chunk returned by retriever is exp_0
    retrieved_chunk = EvidenceChunk(
        chunk_id="exp_0",
        section="experience",
        title="Streaming Engineer",
        organization="DataStream",
        timeframe="2022",
        content="Role: Streaming Engineer at DataStream\nBuilt real-time Kafka consumers with 10k messages per second.",
    )

    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = [(retrieved_chunk, 0.88)]

    # Model hallucinates a citation with invalid source_id 'exp_999'
    mock_ai = MagicMock()
    mock_ai.generate_structured.return_value = CandidateEvidenceAIResult(
        has_evidence=True,
        confidence=EvidenceConfidence.HIGH,
        answer="The candidate has high-scale Kafka experience.",
        citations=[
            EvidenceCitation(
                source_id="exp_999",  # Invalid ID!
                section="experience",
                quote="Built real-time Kafka consumers",
            )
        ],
    )

    service = CandidateEvidenceRAGService(
        retriever=mock_retriever,
        ai_service=mock_ai,
    )

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.rag.service.get_active_resume", lambda db, candidate: resume)

        response = service.ask_candidate_evidence(
            db=db,
            recruiter=recruiter,
            job=job,
            candidate_id=candidate.id,
            request=CandidateEvidenceQueryRequest(query="Kafka experience"),
        )

        # Because the only citation had an invalid source_id, it is discarded,
        # and has_evidence is demoted to False with confidence 'none'
        assert response.has_evidence is False
        assert response.confidence == "none"
        assert response.citations == []
        assert "no verifiable textual quotations" in response.answer.lower()


def test_rag_service_rejects_fabricated_quotation():
    """Citations containing quotes that do not appear in the source chunk content are discarded."""
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=True, title="Backend Dev")
    candidate = Candidate(id=uuid4(), user_id=uuid4(), first_name="Aarav", last_name="Sharma")

    resume_data = ResumeData(
        experience=[
            WorkExperience(
                company="DataStream",
                job_title="Streaming Engineer",
                description="Built real-time Kafka consumers with 10k messages per second.",
            )
        ]
    )
    resume = Resume(
        id=uuid4(),
        candidate_id=candidate.id,
        parsing_status="COMPLETED",
        parsed_data=resume_data.model_dump(),
        is_active=True,
    )

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = candidate

    retrieved_chunk = EvidenceChunk(
        chunk_id="exp_0",
        section="experience",
        title="Streaming Engineer",
        organization="DataStream",
        timeframe="2022",
        content="Role: Streaming Engineer at DataStream\nBuilt real-time Kafka consumers with 10k messages per second.",
    )

    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = [(retrieved_chunk, 0.88)]

    # Model hallucinates a quote not in the chunk: "Managed 500 Kubernetes clusters"
    mock_ai = MagicMock()
    mock_ai.generate_structured.return_value = CandidateEvidenceAIResult(
        has_evidence=True,
        confidence=EvidenceConfidence.HIGH,
        answer="The candidate managed clusters.",
        citations=[
            EvidenceCitation(
                source_id="exp_0",
                section="experience",
                quote="Managed 500 Kubernetes clusters",  # Fabricated quote!
            )
        ],
    )

    service = CandidateEvidenceRAGService(
        retriever=mock_retriever,
        ai_service=mock_ai,
    )

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.rag.service.get_active_resume", lambda db, candidate: resume)

        response = service.ask_candidate_evidence(
            db=db,
            recruiter=recruiter,
            job=job,
            candidate_id=candidate.id,
            request=CandidateEvidenceQueryRequest(query="Kubernetes clusters"),
        )

        assert response.has_evidence is False
        assert response.confidence == "none"
        assert response.citations == []


def test_rag_service_happy_path_with_verified_citations():
    """Happy path: valid citation matches source chunk content exactly."""
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=True, title="Backend Dev")
    candidate = Candidate(id=uuid4(), user_id=uuid4(), first_name="Aarav", last_name="Sharma")

    resume_data = ResumeData(
        experience=[
            WorkExperience(
                company="DataStream",
                job_title="Streaming Engineer",
                description="Built real-time Kafka consumers processing 10k messages per second.",
            )
        ]
    )
    resume = Resume(
        id=uuid4(),
        candidate_id=candidate.id,
        parsing_status="COMPLETED",
        parsed_data=resume_data.model_dump(),
        is_active=True,
    )

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = candidate

    retrieved_chunk = EvidenceChunk(
        chunk_id="exp_0",
        section="experience",
        title="Streaming Engineer",
        organization="DataStream",
        timeframe="2022 - Present",
        content="Role: Streaming Engineer at DataStream\nTimeframe: 2022 - Present\nBuilt real-time Kafka consumers processing 10k messages per second.",
    )

    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = [(retrieved_chunk, 0.91)]

    exact_quote = "Built real-time Kafka consumers processing 10k messages per second."
    mock_ai = MagicMock()
    mock_ai.generate_structured.return_value = CandidateEvidenceAIResult(
        has_evidence=True,
        confidence=EvidenceConfidence.HIGH,
        answer="The candidate has direct experience building high-throughput Kafka streaming pipelines.",
        citations=[
            EvidenceCitation(
                source_id="exp_0",
                section="experience",
                organization="DataStream",
                role="Streaming Engineer",
                timeframe="2022 - Present",
                quote=exact_quote,
            )
        ],
    )

    service = CandidateEvidenceRAGService(
        retriever=mock_retriever,
        ai_service=mock_ai,
    )

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.rag.service.get_active_resume", lambda db, candidate: resume)

        response = service.ask_candidate_evidence(
            db=db,
            recruiter=recruiter,
            job=job,
            candidate_id=candidate.id,
            request=CandidateEvidenceQueryRequest(query="Kafka streaming experience"),
        )

        assert response.has_evidence is True
        assert response.confidence == "high"
        assert len(response.citations) == 1
        assert response.citations[0].source_id == "exp_0"
        assert response.citations[0].quote == exact_quote
        assert response.citations[0].organization == "DataStream"
        assert response.retrieved_chunk_count == 1
        assert "strictly from the candidate's active resume" in response.disclaimer


def test_rag_service_does_not_mutate_database():
    """Verify that RAG queries never call db.commit, db.add, or db.flush."""
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=True, title="Backend Dev")
    candidate = Candidate(id=uuid4(), user_id=uuid4(), first_name="Aarav", last_name="Sharma")

    resume_data = ResumeData(skills=["Python"])
    resume = Resume(
        id=uuid4(),
        candidate_id=candidate.id,
        parsing_status="COMPLETED",
        parsed_data=resume_data.model_dump(),
        is_active=True,
    )

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = candidate

    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = []

    service = CandidateEvidenceRAGService(retriever=mock_retriever)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.rag.service.get_active_resume", lambda db, candidate: resume)

        service.ask_candidate_evidence(
            db=db,
            recruiter=recruiter,
            job=job,
            candidate_id=candidate.id,
            request=CandidateEvidenceQueryRequest(query="Database"),
        )

    db.commit.assert_not_called()
    db.add.assert_not_called()
    db.flush.assert_not_called()


def test_rag_service_partial_citation_failure_fails_closed():
    """
    If multiple citations are returned by the LLM and any citation fails validation
    (e.g. 1 valid citation, 1 fabricated citation), the service must fail closed with an
    insufficient-evidence response to ensure unverified claims cannot persist in the answer prose.
    """
    recruiter = Recruiter(id=uuid4(), user_id=uuid4())
    job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=True, title="Backend Dev")
    candidate = Candidate(id=uuid4(), user_id=uuid4(), first_name="Aarav", last_name="Sharma")

    resume_data = ResumeData(
        experience=[
            WorkExperience(
                company="DataStream",
                job_title="Streaming Engineer",
                description="Built real-time Kafka consumers with 10k messages per second.",
            )
        ]
    )
    resume = Resume(
        id=uuid4(),
        candidate_id=candidate.id,
        parsing_status="COMPLETED",
        parsed_data=resume_data.model_dump(),
        is_active=True,
    )

    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = candidate

    retrieved_chunk = EvidenceChunk(
        chunk_id="exp_0",
        section="experience",
        title="Streaming Engineer",
        organization="DataStream",
        timeframe="2022",
        content="Role: Streaming Engineer at DataStream\nBuilt real-time Kafka consumers with 10k messages per second.",
    )

    mock_retriever = MagicMock()
    mock_retriever.retrieve.return_value = [(retrieved_chunk, 0.88)]

    # Model returns 2 citations: 1 valid, 1 fabricated
    mock_ai = MagicMock()
    mock_ai.generate_structured.return_value = CandidateEvidenceAIResult(
        has_evidence=True,
        confidence=EvidenceConfidence.HIGH,
        answer="The candidate has Kafka experience and also architected globally distributed Cassandra databases.",
        citations=[
            EvidenceCitation(
                source_id="exp_0",
                section="experience",
                quote="Built real-time Kafka consumers with 10k messages per second.",  # VALID
            ),
            EvidenceCitation(
                source_id="exp_0",
                section="experience",
                quote="architected globally distributed Cassandra databases",  # FABRICATED QUOTE!
            ),
        ],
    )

    service = CandidateEvidenceRAGService(
        retriever=mock_retriever,
        ai_service=mock_ai,
    )

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("app.ai.rag.service.get_active_resume", lambda db, candidate: resume)

        response = service.ask_candidate_evidence(
            db=db,
            recruiter=recruiter,
            job=job,
            candidate_id=candidate.id,
            request=CandidateEvidenceQueryRequest(query="Kafka and Cassandra experience"),
        )

        # Partial failure must fail closed:
        assert response.has_evidence is False
        assert response.confidence == "none"
        assert response.citations == []
        assert "failed verification" in response.answer.lower()
