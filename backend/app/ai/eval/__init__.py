"""
Hirely AI Evaluation Framework.
Provides versioned dataset schemas, deterministic retrieval/generation metrics,
offline test runner, and optional live Ragas quality benchmarking.
"""

from app.ai.eval.ragas_adapter import CandidateEvidenceRagasAdapter, is_ragas_available
from app.ai.eval.schemas import (
    CaseEvaluationResult,
    EvaluationReport,
    ExpectedCitation,
    RAGEvalCase,
    RAGEvaluationDataset,
    SecurityExpectations,
)

__all__ = [
    "ExpectedCitation",
    "SecurityExpectations",
    "RAGEvalCase",
    "RAGEvaluationDataset",
    "CaseEvaluationResult",
    "EvaluationReport",
    "is_ragas_available",
    "CandidateEvidenceRagasAdapter",
]
