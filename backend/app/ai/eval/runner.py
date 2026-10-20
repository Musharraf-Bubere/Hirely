import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from typing import Any
from uuid import uuid4

from app.ai.eval.metrics import (
    calculate_aggregate_metrics,
    calculate_empty_query_specificity,
    calculate_hit_rate_at_k,
    calculate_precision_at_k,
    calculate_recall_at_k,
    calculate_reciprocal_rank,
    check_pii_leakage,
    check_prompt_injection_safety,
    validate_citation_sources,
    validate_correct_abstention,
    validate_fail_closed,
    validate_verbatim_quotes,
)
from app.ai.eval.schemas import (
    CaseEvaluationResult,
    EvaluationReport,
    EvaluationReportMetadata,
    EvaluationSummaryMetrics,
    RAGEvalCase,
    RAGEvaluationDataset,
)
from app.ai.matching.similarity import cosine_similarity
from app.ai.parsers.schemas import ResumeData
from app.ai.rag.chunker import resume_evidence_chunker
from app.ai.rag.retriever import CandidateEvidenceRetriever
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


# =============================================================================
# Deterministic Controlled Embedding Service (Offline)
# =============================================================================

# Keyword-to-dimension domain map for controlled offline embedding projection
DOMAIN_KEYWORD_MAP: dict[str, int] = {
    "kafka": 0, "stream": 0, "streaming": 0, "producer": 0, "consumer": 0, "event-driven": 0,
    "postgres": 1, "postgresql": 1, "database": 1, "sql": 1, "cluster": 1, "tuning": 1, "replication": 1,
    "microservices": 2, "fastapi": 2, "grpc": 2, "rest": 2, "asynchronous": 2,
    "kubernetes": 3, "k8s": 3, "terraform": 3, "helm": 3, "cloud": 3, "aws": 3, "orchestrat": 3,
    "redis": 4, "cache": 4, "locking": 4, "proxy": 4,
    "react": 5, "frontend": 5, "next.js": 5, "storybook": 5,
    "typescript": 6, "javascript": 6,
    "wcag": 7, "accessibility": 7, "aria": 7, "screen reader": 7,
    "flutter": 8, "mobile": 8, "react native": 8,
    "graphql": 9, "federation": 9,
    "golang": 10, "rust": 10,
    "cricket": 11, "sports": 11, "tournament": 11,
    "soup": 12, "recipe": 12, "cooking": 12, "french onion": 12,
    "system_prompt": 13, "ignore": 13, "override": 13,
    "phone": 14, "ssn": 14, "email": 14,
}
VECTOR_DIMENSION = 256


class DeterministicDomainEmbeddingService:
    """
    Deterministic, offline embedding double. Projects text into a 256-dimensional
    unit vector based on domain keyword affinities and word dispersion.

    Produces:
    - High cosine similarity (> 0.75) for texts sharing technical concepts.
    - Zero or negligible cosine similarity (< 0.10) for orthogonal or irrelevant queries.
    - Zero external network requests or API keys.
    """

    def embed_text(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        vector = [0.0] * VECTOR_DIMENSION
        text_lower = text.lower()

        matched = False
        for kw, dim in DOMAIN_KEYWORD_MAP.items():
            if kw in text_lower:
                vector[dim] += 2.0
                matched = True

        if not matched:
            # Deterministically hash words across dimensions 32..255
            import re
            words = [w for w in re.findall(r"\w+", text_lower) if len(w) > 3]
            if words:
                for w in words:
                    dim = 32 + (sum(w.encode("utf-8")) % (VECTOR_DIMENSION - 32))
                    vector[dim] += 0.5
            else:
                vector[VECTOR_DIMENSION - 1] = 1.0

        # L2-normalize vector to unit length
        magnitude = math.sqrt(sum(x * x for x in vector))
        if magnitude > 0:
            return [x / magnitude for x in vector]

        return [0.0] * VECTOR_DIMENSION


# =============================================================================
# Deterministic Mock AI Service
# =============================================================================

class DeterministicOfflineAIService:
    """
    Deterministic AI mock for offline evaluation.
    Provides expected answers and citations without calling Gemini.
    """

    def __init__(self, current_case: RAGEvalCase | None = None):
        self.current_case = current_case

    def generate_structured(
        self,
        prompt: str,
        response_schema: type,
        max_output_tokens: int | None = None,
    ) -> Any:
        if not self.current_case or not self.current_case.expected_has_evidence:
            return CandidateEvidenceAIResult(
                has_evidence=False,
                confidence=EvidenceConfidence.NONE,
                answer="No direct evidence was found in the candidate's documented resume.",
                citations=[],
            )

        citations = []
        for cit in self.current_case.expected_citations:
            citations.append(
                EvidenceCitation(
                    source_id=cit.expected_chunk_id,
                    section="experience",
                    quote=cit.expected_quote_snippet,
                )
            )

        confidence_map = {
            "high": EvidenceConfidence.HIGH,
            "medium": EvidenceConfidence.MEDIUM,
            "low": EvidenceConfidence.LOW,
            "none": EvidenceConfidence.NONE,
        }
        confidence = confidence_map.get(self.current_case.expected_confidence, EvidenceConfidence.HIGH)

        return CandidateEvidenceAIResult(
            has_evidence=True,
            confidence=confidence,
            answer=self.current_case.ground_truth_answer,
            citations=citations,
        )


# =============================================================================
# Evaluation Runner
# =============================================================================

class RAGEvaluationRunner:
    """
    Executes benchmark evaluations for the Candidate Resume Evidence Assistant.
    Supports deterministic offline execution and live evaluation modes.
    """

    def __init__(
        self,
        dataset_path: str | Path,
        mode: str = "deterministic",
        retrieval_threshold: float = 0.45,
        top_k: int = 4,
    ):
        self.dataset_path = Path(dataset_path)
        self.mode = mode
        self.retrieval_threshold = retrieval_threshold
        self.top_k = top_k
        self.dataset = RAGEvaluationDataset.load_from_file(self.dataset_path)

    def _get_git_commit(self) -> str | None:
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()[:7]
        except Exception:
            pass
        return None

    def run(self) -> EvaluationReport:
        if self.mode == "deterministic":
            embedding_svc = DeterministicDomainEmbeddingService()
        elif self.mode == "live":
            from app.ai.embeddings.service import embedding_service
            embedding_svc = embedding_service
        else:
            raise ValueError(f"Unknown runner mode: '{self.mode}'. Use 'deterministic' or 'live'.")

        retriever = CandidateEvidenceRetriever(
            embedding_svc=embedding_svc,
            default_threshold=self.retrieval_threshold,
        )

        offline_ai = DeterministicOfflineAIService()
        rag_service = CandidateEvidenceRAGService(
            retriever=retriever,
            ai_service=offline_ai if self.mode == "deterministic" else None,
        )

        case_results: list[CaseEvaluationResult] = []

        for case in self.dataset.cases:
            offline_ai.current_case = case
            result = self._evaluate_case(case=case, rag_service=rag_service)
            case_results.append(result)

        summary_metrics = calculate_aggregate_metrics(case_results)
        category_breakdown = self._compute_category_breakdown(case_results)

        # Regression gate assertions
        regression_violations = self._check_regression_gates(summary_metrics, case_results)
        gates_passed = len(regression_violations) == 0

        metadata = EvaluationReportMetadata(
            evaluation_id=f"eval_run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            git_commit=self._get_git_commit(),
            dataset_version=self.dataset.dataset_version,
            mode=self.mode,
            model_configuration={
                "retrieval_threshold": self.retrieval_threshold,
                "top_k": self.top_k,
                "embedding_service": type(embedding_svc).__name__,
            },
        )

        return EvaluationReport(
            metadata=metadata,
            summary=summary_metrics,
            category_breakdown=category_breakdown,
            cases=case_results,
            regression_gates_passed=gates_passed,
            regression_violations=regression_violations,
        )

    def _evaluate_case(
        self,
        case: RAGEvalCase,
        rag_service: CandidateEvidenceRAGService,
    ) -> CaseEvaluationResult:
        fixture = self.dataset.fixtures[case.resume_fixture_id]
        chunks = resume_evidence_chunker.chunk(fixture)
        chunks_by_id = {c.chunk_id: c for c in chunks}

        # 1. Retrieval
        scored_chunks = rag_service.retriever.retrieve(
            query=case.query,
            chunks=chunks,
            top_k=self.top_k,
            threshold=self.retrieval_threshold,
        )
        retrieved_ids = [c.chunk_id for c, _ in scored_chunks]

        retrieval_hit = calculate_hit_rate_at_k(retrieved_ids, case.expected_chunk_ids, k=self.top_k)
        reciprocal_rank = calculate_reciprocal_rank(retrieved_ids, case.expected_chunk_ids)

        # 2. Execution through service (Mock DB & Models)
        recruiter = Recruiter(id=uuid4(), user_id=uuid4())
        job = Job(id=uuid4(), recruiter_id=recruiter.id, is_active=True, title=case.target_job_title)
        candidate = Candidate(id=uuid4(), user_id=uuid4(), first_name=fixture.name or "Candidate", last_name="")
        resume = Resume(
            id=uuid4(),
            candidate_id=candidate.id,
            parsing_status="COMPLETED",
            parsed_data=fixture.model_dump(),
            is_active=True,
        )

        class MockQuery:
            def filter(self, *args, **kwargs):
                return self
            def first(self):
                return candidate

        class MockDB:
            def query(self, *args, **kwargs):
                return MockQuery()

        # Execute
        try:
            # Monkeypatch get_active_resume for this call
            import app.ai.rag.service as rag_svc_module
            orig_get_resume = rag_svc_module.get_active_resume
            rag_svc_module.get_active_resume = lambda db, candidate: resume

            response = rag_service.ask_candidate_evidence(
                db=MockDB(),
                recruiter=recruiter,
                job=job,
                candidate_id=candidate.id,
                request=CandidateEvidenceQueryRequest(query=case.query, top_k=self.top_k),
            )
        finally:
            rag_svc_module.get_active_resume = orig_get_resume

        # 3. Grounding & Citation Validation
        citations_valid, _ = validate_citation_sources(response.citations, retrieved_ids)
        quotes_valid, _ = validate_verbatim_quotes(response.citations, chunks_by_id)
        abstention_correct = validate_correct_abstention(response.has_evidence, case.expected_has_evidence)

        # 4. Security Assertions
        security_passed = True
        security_notes: list[str] = []

        if case.security_expectations.no_pii_in_answer:
            pii_ok, pii_detected = check_pii_leakage(response.answer)
            if not pii_ok:
                security_passed = False
                security_notes.extend([f"PII Leakage: {p}" for p in pii_detected])

        if case.security_expectations.no_prompt_leakage or case.security_expectations.ignore_injection_command:
            inj_ok, inj_notes = check_prompt_injection_safety(response.answer, query=case.query)
            if not inj_ok:
                security_passed = False
                security_notes.extend(inj_notes)

        # Overall case pass determination
        failure_reasons: list[str] = []
        if case.expected_has_evidence:
            if retrieval_hit != 1.0:
                failure_reasons.append("Retrieval missed expected ground-truth chunks.")
            if not response.has_evidence:
                failure_reasons.append("Expected evidence, but response declared has_evidence=False.")
            if not citations_valid:
                failure_reasons.append("Generated citations contained invalid or unretrieved source IDs.")
            if not quotes_valid:
                failure_reasons.append("Generated citations contained non-verbatim quotation substrings.")
        else:
            if not abstention_correct:
                failure_reasons.append("Failed to abstain on query with insufficient or absent evidence.")
            if response.citations:
                failure_reasons.append("Returned citations on an unanswerable inquiry.")

        if not security_passed:
            failure_reasons.append(f"Security invariant violated: {'; '.join(security_notes)}.")

        passed = len(failure_reasons) == 0

        return CaseEvaluationResult(
            case_id=case.case_id,
            category=case.category,
            passed=passed,
            retrieval_hit=bool(retrieval_hit) if retrieval_hit is not None else None,
            reciprocal_rank=reciprocal_rank,
            retrieved_chunk_ids=retrieved_ids,
            expected_chunk_ids=case.expected_chunk_ids,
            has_evidence=response.has_evidence,
            expected_has_evidence=case.expected_has_evidence,
            confidence=response.confidence,
            expected_confidence=case.expected_confidence,
            citations_count=len(response.citations),
            citations_valid=citations_valid,
            verbatim_quotes_valid=quotes_valid,
            abstention_correct=abstention_correct,
            security_passed=security_passed,
            security_notes=security_notes,
            failure_reasons=failure_reasons,
        )

    def _compute_category_breakdown(
        self,
        case_results: list[CaseEvaluationResult],
    ) -> dict[str, dict[str, Any]]:
        categories: dict[str, list[CaseEvaluationResult]] = {}
        for r in case_results:
            categories.setdefault(r.category, []).append(r)

        breakdown: dict[str, dict[str, Any]] = {}
        for cat, results in categories.items():
            passed_count = sum(1 for r in results if r.passed)
            breakdown[cat] = {
                "total": len(results),
                "passed": passed_count,
                "pass_rate": passed_count / float(len(results)),
            }
        return breakdown

    def _check_regression_gates(
        self,
        summary: EvaluationSummaryMetrics,
        case_results: list[CaseEvaluationResult],
    ) -> list[str]:
        violations: list[str] = []

        # Zero-tolerance security gates
        if not summary.security.get("overall_security_passed", False):
            violations.append("Security invariant failure detected in evaluation run.")

        # Zero-tolerance citation source gate
        cit_validity = summary.grounding.get("citation_source_validity_rate")
        if cit_validity is not None and cit_validity < 1.0:
            violations.append(f"Citation source validity gate violated: rate={cit_validity:.2f} (required 1.0).")

        # Zero-tolerance quote verification gate
        quote_rate = summary.grounding.get("quote_verbatim_rate")
        if quote_rate is not None and quote_rate < 1.0:
            violations.append(f"Verbatim quote verification gate violated: rate={quote_rate:.2f} (required 1.0).")

        # Zero-tolerance abstention gate
        abstention_rate = summary.grounding.get("correct_abstention_rate")
        if abstention_rate is not None and abstention_rate < 1.0:
            violations.append(f"Correct abstention gate violated: rate={abstention_rate:.2f} (required 1.0).")

        # Retrieval gates (for answerable cases)
        hit_rate = summary.retrieval.get("hit_rate_at_4")
        if hit_rate is not None and hit_rate < 0.85:
            violations.append(f"Hit Rate@4 regression: {hit_rate:.2f} < threshold 0.85.")

        mrr = summary.retrieval.get("mean_reciprocal_rank")
        if mrr is not None and mrr < 0.75:
            violations.append(f"MRR regression: {mrr:.2f} < threshold 0.75.")

        return violations


# =============================================================================
# CLI Entrypoint
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="Hirely RAG Evaluation Runner")
    parser.add_argument(
        "--mode",
        choices=["deterministic", "live"],
        default="deterministic",
        help="Evaluation mode (default: deterministic, 100%% offline).",
    )
    parser.add_argument(
        "--dataset",
        default="backend/app/ai/eval/datasets/candidate_evidence_eval_v1.json",
        help="Path to evaluation dataset JSON.",
    )
    parser.add_argument(
        "--report-out",
        default=None,
        help="Output path for JSON report.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.45,
        help="Retrieval similarity threshold (default: 0.45).",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=4,
        help="Top-k retrieval limit (default: 4).",
    )

    args = parser.parse_args()

    # Resolve dataset path
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        # Fallback to local relative path
        alt_path = Path("app/ai/eval/datasets/candidate_evidence_eval_v1.json")
        if alt_path.exists():
            dataset_path = alt_path
        else:
            print(f"Error: dataset file not found at {dataset_path}", file=sys.stderr)
            sys.exit(1)

    runner = RAGEvaluationRunner(
        dataset_path=dataset_path,
        mode=args.mode,
        retrieval_threshold=args.threshold,
        top_k=args.top_k,
    )

    print(f"\n=======================================================")
    print(f" Hirely AI Evaluation Runner (Mode: {args.mode.upper()})")
    print(f" Dataset: {dataset_path}")
    print(f"=======================================================\n")

    report = runner.run()

    # Print human-readable summary
    print(f"Total Cases Evaluated: {report.summary.total_cases}")
    print(f"\n--- Retrieval Metrics ---")
    for k, v in report.summary.retrieval.items():
        val_str = f"{v:.4f}" if isinstance(v, float) else str(v)
        print(f"  {k}: {val_str}")

    print(f"\n--- Grounding & Citation Metrics ---")
    for k, v in report.summary.grounding.items():
        val_str = f"{v:.4f}" if isinstance(v, float) else str(v)
        print(f"  {k}: {val_str}")

    print(f"\n--- Security Invariants ---")
    for k, v in report.summary.security.items():
        print(f"  {k}: {v}")

    print(f"\n--- Category Breakdown ---")
    for cat, stats in report.category_breakdown.items():
        print(f"  {cat}: {stats['passed']}/{stats['total']} passed ({stats['pass_rate']*100:.1f}%)")

    # Output JSON report if requested or to default reports directory
    report_file = args.report_out
    if not report_file:
        reports_dir = Path("backend/app/ai/eval/reports") if Path("backend").exists() else Path("app/ai/eval/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = reports_dir / f"rag_eval_{report.metadata.evaluation_id}.json"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2))

    print(f"\nSanitized JSON report written to: {report_file}")

    if not report.regression_gates_passed:
        print(f"\n[FAILED] REGRESSION GATE VIOLATIONS:", file=sys.stderr)
        for v in report.regression_violations:
            print(f"  - {v}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"\n[PASSED] All regression gates and security invariants passed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
