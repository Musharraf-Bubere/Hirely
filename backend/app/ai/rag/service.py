from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.parsers.schemas import ResumeData
from app.ai.rag.chunker import ResumeEvidenceChunker, resume_evidence_chunker
from app.ai.rag.prompts import EvidenceRAGPromptBuilder, evidence_rag_prompt_builder
from app.ai.rag.retriever import CandidateEvidenceRetriever, candidate_evidence_retriever
from app.ai.rag.schemas import (
    CandidateEvidenceAIResult,
    CandidateEvidenceQueryRequest,
    CandidateEvidenceResponse,
    EvidenceCitation,
    EvidenceConfidence,
)
from app.ai.services.gemini_service import GeminiService, gemini_service
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.services.resume import get_active_resume


class CandidateEvidenceRAGService:
    """
    Orchestrates the Candidate Resume Evidence Assistant:
    - Authorizes recruiter ownership of the target job.
    - Chunks candidate's active resume.
    - Retrieves top-k relevant chunks matching the recruiter's query.
    - Prompts Gemini with strict anti-fabrication guidelines.
    - Programmatically validates citation sources and verbatim quotes.
    - Guarantees read-only execution with zero database mutations.
    """

    def __init__(
        self,
        chunker: ResumeEvidenceChunker | None = None,
        retriever: CandidateEvidenceRetriever | None = None,
        prompt_builder: EvidenceRAGPromptBuilder | None = None,
        ai_service: GeminiService | None = None,
    ):
        self.chunker = chunker or resume_evidence_chunker
        self.retriever = retriever or candidate_evidence_retriever
        self.prompt_builder = prompt_builder or evidence_rag_prompt_builder
        self.ai_service = ai_service or gemini_service

    def ask_candidate_evidence(
        self,
        *,
        db: Session,
        recruiter: Recruiter,
        job: Job,
        candidate_id: UUID,
        request: CandidateEvidenceQueryRequest,
    ) -> CandidateEvidenceResponse:
        # 1. Authorization & Job Validation
        if job.recruiter_id != recruiter.id:
            raise ValueError("You do not have permission to query candidate evidence for this job.")

        if not job.is_active:
            raise ValueError("Target job is inactive.")

        # 2. Candidate & Active Resume Retrieval
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if not candidate:
            raise ValueError("Candidate not found.")

        resume = get_active_resume(db=db, candidate=candidate)
        if not resume:
            raise ValueError("Candidate does not have an active resume.")

        if resume.parsing_status != "COMPLETED" or not resume.parsed_data:
            raise ValueError("Candidate active resume has not been parsed successfully.")

        try:
            resume_data = ResumeData.model_validate(resume.parsed_data)
        except Exception as exc:
            raise ValueError("Candidate resume parsed data is invalid or corrupt.") from exc

        # 3. Chunking
        chunks = self.chunker.chunk(resume_data)
        if not chunks:
            return CandidateEvidenceResponse(
                candidate_id=candidate.id,
                job_id=job.id,
                query=request.query,
                has_evidence=False,
                confidence=EvidenceConfidence.NONE.value,
                answer=f"The candidate's resume contains no documented sections to evaluate '{request.query}'.",
                citations=[],
                retrieved_chunk_count=0,
            )

        # 4. Retrieval & Relevance Filtering
        scored_chunks = self.retriever.retrieve(
            query=request.query,
            chunks=chunks,
            top_k=request.top_k,
        )

        # If no chunks met the relevance threshold, do not ask Gemini to invent an answer
        if not scored_chunks:
            return CandidateEvidenceResponse(
                candidate_id=candidate.id,
                job_id=job.id,
                query=request.query,
                has_evidence=False,
                confidence=EvidenceConfidence.NONE.value,
                answer=f"No direct evidence addressing '{request.query}' was found in the candidate's documented resume.",
                citations=[],
                retrieved_chunk_count=0,
            )

        retrieved_chunks = [c for c, _ in scored_chunks]
        retrieved_chunks_by_id = {c.chunk_id: c for c in retrieved_chunks}

        # 5. Prompt Construction & Gemini Structured Generation
        candidate_name = f"{candidate.first_name} {candidate.last_name}".strip()
        prompt = self.prompt_builder.build_prompt(
            candidate_name=candidate_name,
            job_title=job.title,
            query=request.query,
            chunks=retrieved_chunks,
        )

        ai_result: CandidateEvidenceAIResult = self.ai_service.generate_structured(
            prompt=prompt,
            response_schema=CandidateEvidenceAIResult,
        )

        # 6. Strict Code-Enforced Citation Validation & Anti-Hallucination Guardrails
        valid_citations: list[EvidenceCitation] = []

        if ai_result.has_evidence and ai_result.citations:
            for cit in ai_result.citations:
                # Rule 1: Citation source ID must belong to retrieved chunks
                if cit.source_id not in retrieved_chunks_by_id:
                    continue

                source_chunk = retrieved_chunks_by_id[cit.source_id]

                # Rule 2: Quote must be an exact substring of the source chunk's content
                cleaned_quote = cit.quote.strip() if cit.quote else ""
                if not cleaned_quote:
                    continue

                # Case-insensitive substring check with normalized spaces
                norm_quote = " ".join(cleaned_quote.lower().split())
                norm_content = " ".join(source_chunk.content.lower().split())

                if norm_quote not in norm_content:
                    # Fabricated or inaccurate quotation rejected
                    continue

                # Valid citation with verified provenance metadata
                valid_citations.append(
                    EvidenceCitation(
                        source_id=cit.source_id,
                        section=source_chunk.section,
                        organization=source_chunk.organization or cit.organization,
                        role=source_chunk.title or cit.role,
                        timeframe=source_chunk.timeframe or cit.timeframe,
                        quote=cit.quote.strip(),
                    )
                )

        # Fail-closed citation safety:
        # If the model claimed evidence, every single citation must survive source and quote validation.
        # If any citation was invalid (partial failure) or zero citations survived, we cannot guarantee
        # that the model's synthesized answer prose is free of unsupported or fabricated claims.
        # Therefore, we fail closed with an insufficient-evidence response rather than returning
        # a potentially misleading answer.
        had_invalid_citation = (
            ai_result.has_evidence
            and bool(ai_result.citations)
            and len(valid_citations) < len(ai_result.citations)
        )

        if ai_result.has_evidence and not valid_citations:
            has_evidence = False
            confidence = EvidenceConfidence.NONE.value
            valid_citations = []
            answer = (
                f"Although potential relevance was detected, no verifiable textual quotations could be confirmed in the "
                f"candidate's resume to substantiate claims regarding '{request.query}'."
            )
        elif had_invalid_citation:
            has_evidence = False
            confidence = EvidenceConfidence.NONE.value
            valid_citations = []
            answer = (
                f"Evidence could not be reliably verified from the candidate's documented resume for '{request.query}'. "
                f"One or more citation sources or quotes failed verification."
            )
        elif not ai_result.has_evidence:
            has_evidence = False
            confidence = EvidenceConfidence.NONE.value
            valid_citations = []
            answer = ai_result.answer
        else:
            confidence = (
                ai_result.confidence.value
                if hasattr(ai_result.confidence, "value")
                else str(ai_result.confidence).lower()
            )
            if confidence == EvidenceConfidence.NONE.value:
                has_evidence = False
                valid_citations = []
                answer = ai_result.answer
            else:
                has_evidence = True
                answer = ai_result.answer

        return CandidateEvidenceResponse(
            candidate_id=candidate.id,
            job_id=job.id,
            query=request.query,
            has_evidence=has_evidence,
            confidence=confidence,
            answer=answer,
            citations=valid_citations,
            retrieved_chunk_count=len(scored_chunks),
        )


candidate_evidence_rag_service = CandidateEvidenceRAGService()
