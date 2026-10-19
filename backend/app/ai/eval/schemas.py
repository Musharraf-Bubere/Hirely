import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator

from app.ai.parsers.schemas import ResumeData


class ExpectedCitation(BaseModel):
    expected_chunk_id: str = Field(
        description="Chunk ID expected to support this statement, e.g. exp_0, proj_1.",
    )
    expected_quote_snippet: str = Field(
        description="Key substring phrase expected to appear verbatim in citation quote.",
    )


class SecurityExpectations(BaseModel):
    no_pii_in_answer: bool = Field(
        default=True,
        description="Asserts candidate email and phone do not appear in generated answer/citations.",
    )
    no_prompt_leakage: bool = Field(
        default=True,
        description="Asserts internal system prompts or instructions are not leaked.",
    )
    ignore_injection_command: bool = Field(
        default=True,
        description="Asserts prompt injection instructions inside query or resume are ignored.",
    )
    fail_closed_if_invalid_citation: bool = Field(
        default=True,
        description="Asserts service fails closed (has_evidence=False) if citations are invalid.",
    )


class RAGEvalCase(BaseModel):
    case_id: str = Field(min_length=3, description="Unique case identifier, e.g. case_01_kafka_direct.")
    category: str = Field(
        description=(
            "Evaluation category: answerable_direct, answerable_multi_chunk, paraphrased_query, "
            "insufficient_evidence, irrelevant_query, fabricated_citation_attempt, "
            "prompt_injection_question, prompt_injection_resume, pii_leakage_check."
        ),
    )
    query: str = Field(min_length=3, description="Recruiter inquiry question.")
    target_job_title: str = Field(min_length=2, description="Target job context title.")
    resume_fixture_id: str = Field(min_length=1, description="Identifier of the synthetic resume fixture.")
    expected_chunk_ids: list[str] = Field(
        default_factory=list,
        description="Ground-truth list of relevant chunk IDs (independent of retriever results).",
    )
    expected_has_evidence: bool = Field(
        description="Whether verifiable evidence exists in the candidate's documented resume.",
    )
    expected_confidence: str = Field(
        description="Expected confidence: 'high', 'medium', 'low', or 'none'.",
    )
    ground_truth_answer: str = Field(
        min_length=5,
        description="Reference ground-truth answer for comparison.",
    )
    expected_citations: list[ExpectedCitation] = Field(
        default_factory=list,
        description="Expected ground-truth citations supporting the answer.",
    )
    security_expectations: SecurityExpectations = Field(
        default_factory=SecurityExpectations,
    )

    @model_validator(mode="after")
    def validate_ground_truth_consistency(self) -> "RAGEvalCase":
        # Contradiction check 1: False evidence with chunks or non-none confidence
        if not self.expected_has_evidence:
            if self.expected_confidence != "none":
                raise ValueError(
                    f"Case '{self.case_id}' has expected_has_evidence=False, "
                    f"so expected_confidence must be 'none', got '{self.expected_confidence}'."
                )
            if self.expected_chunk_ids:
                raise ValueError(
                    f"Case '{self.case_id}' has expected_has_evidence=False, "
                    f"so expected_chunk_ids must be empty, got {self.expected_chunk_ids}."
                )
            if self.expected_citations:
                raise ValueError(
                    f"Case '{self.case_id}' has expected_has_evidence=False, "
                    f"so expected_citations must be empty."
                )
        else:
            # Contradiction check 2: True evidence without chunks or with none confidence
            if self.expected_confidence == "none":
                raise ValueError(
                    f"Case '{self.case_id}' has expected_has_evidence=True, "
                    f"so expected_confidence cannot be 'none'."
                )
            if not self.expected_chunk_ids:
                raise ValueError(
                    f"Case '{self.case_id}' has expected_has_evidence=True, "
                    f"so expected_chunk_ids cannot be empty."
                )

        # Expected citations must point to expected chunks
        for cit in self.expected_citations:
            if cit.expected_chunk_id not in self.expected_chunk_ids:
                raise ValueError(
                    f"Case '{self.case_id}' citation references chunk '{cit.expected_chunk_id}' "
                    f"which is not in expected_chunk_ids {self.expected_chunk_ids}."
                )

        return self


class RAGEvaluationDataset(BaseModel):
    dataset_version: str = Field(description="Semantic version of the dataset, e.g. candidate_evidence_eval_v1.")
    description: str = Field(description="High-level description of dataset contents and scope.")
    fixtures: dict[str, ResumeData] = Field(
        description="Mapping of fixture_id to synthetic parsed ResumeData.",
    )
    cases: list[RAGEvalCase] = Field(
        min_length=1,
        description="List of evaluation cases.",
    )

    @model_validator(mode="after")
    def validate_dataset_integrity(self) -> "RAGEvaluationDataset":
        seen_case_ids: set[str] = set()
        for case in self.cases:
            if case.case_id in seen_case_ids:
                raise ValueError(f"Duplicate case_id found in dataset: '{case.case_id}'.")
            seen_case_ids.add(case.case_id)

            if case.resume_fixture_id not in self.fixtures:
                raise ValueError(
                    f"Case '{case.case_id}' references unknown fixture '{case.resume_fixture_id}'. "
                    f"Available fixtures: {list(self.fixtures.keys())}."
                )

        return self

    @classmethod
    def load_from_file(cls, path: str | Path) -> "RAGEvaluationDataset":
        resolved_path = Path(path).resolve()
        if not resolved_path.exists():
            raise FileNotFoundError(f"Evaluation dataset file not found at: {resolved_path}")

        with open(resolved_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        return cls.model_validate(raw_data)


# =============================================================================
# Reporting Schemas
# =============================================================================

class CaseEvaluationResult(BaseModel):
    case_id: str
    category: str
    passed: bool
    retrieval_hit: bool | None = None
    reciprocal_rank: float | None = None
    retrieved_chunk_ids: list[str] = Field(default_factory=list)
    expected_chunk_ids: list[str] = Field(default_factory=list)
    has_evidence: bool
    expected_has_evidence: bool
    confidence: str
    expected_confidence: str
    citations_count: int = 0
    citations_valid: bool = True
    verbatim_quotes_valid: bool = True
    abstention_correct: bool = True
    security_passed: bool = True
    security_notes: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)


class EvaluationSummaryMetrics(BaseModel):
    total_cases: int
    retrieval: dict[str, Any]
    grounding: dict[str, Any]
    security: dict[str, Any]


class EvaluationReportMetadata(BaseModel):
    evaluation_id: str
    timestamp_utc: str
    git_commit: str | None = None
    dataset_version: str
    mode: str
    model_configuration: dict[str, Any]


class EvaluationReport(BaseModel):
    metadata: EvaluationReportMetadata
    summary: EvaluationSummaryMetrics
    category_breakdown: dict[str, dict[str, Any]]
    cases: list[CaseEvaluationResult]
    regression_gates_passed: bool
    regression_violations: list[str] = Field(default_factory=list)
