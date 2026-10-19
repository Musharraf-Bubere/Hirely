from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class EvidenceConfidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class EvidenceChunk(BaseModel):
    chunk_id: str = Field(description="Unique stable identifier for the chunk, e.g. exp_0, proj_1.")
    section: str = Field(description="Resume section: experience, projects, education, certifications, or summary.")
    title: str | None = Field(default=None, description="Job title, project name, degree, or certification name.")
    organization: str | None = Field(default=None, description="Company, organization, institution, or issuer.")
    timeframe: str | None = Field(default=None, description="Employment, study, or issuance timeframe.")
    content: str = Field(description="Substantive text content of the resume entry.")


class CandidateEvidenceQueryRequest(BaseModel):
    query: str = Field(
        min_length=3,
        max_length=500,
        description="The verification question or skill inquiry to ask about the candidate.",
    )
    top_k: int = Field(
        default=4,
        ge=1,
        le=8,
        description="Maximum number of relevant evidence chunks to retrieve and ground the answer on.",
    )


class EvidenceCitation(BaseModel):
    source_id: str = Field(description="Identifier of the retrieved chunk supporting this citation.")
    section: str = Field(description="Section of the supporting chunk.")
    organization: str | None = Field(default=None, description="Company or institution name.")
    role: str | None = Field(default=None, description="Job title, project name, or degree.")
    timeframe: str | None = Field(default=None, description="Dates or timeframe of the supporting experience.")
    quote: str = Field(description="Verbatim excerpt from the source chunk text.")


class CandidateEvidenceAIResult(BaseModel):
    has_evidence: bool = Field(
        description="True if direct, substantive evidence was found in the provided resume chunks.",
    )
    confidence: EvidenceConfidence = Field(
        description="Confidence level in the evidence sufficiency: high, medium, low, or none.",
    )
    answer: str = Field(
        description="Synthesized grounded answer citing specific retrieved chunks.",
    )
    citations: list[EvidenceCitation] = Field(
        default_factory=list,
        description="List of verified citations linking to retrieved chunks.",
    )


class CandidateEvidenceResponse(BaseModel):
    candidate_id: UUID
    job_id: UUID
    query: str
    has_evidence: bool
    confidence: str
    answer: str
    citations: list[EvidenceCitation]
    retrieved_chunk_count: int
    disclaimer: str = Field(
        default=(
            "This answer is synthesized by Hirely RAG strictly from the candidate's active resume. "
            "All citations reference specific documented qualifications without independent external verification."
        ),
        description="Advisory grounding disclaimer.",
    )
