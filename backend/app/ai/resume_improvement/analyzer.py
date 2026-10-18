from pydantic import BaseModel, Field

from app.ai.ats_analyzer.analyzer import (
    ATSDeterministicResult,
    ats_analyzer,
)
from app.ai.ats_analyzer.context import (
    ATSContext,
    ats_context_builder,
)
from app.ai.ats_analyzer.schemas import ATSScoreBreakdown
from app.ai.ats_analyzer.semantic import ats_semantic_analyzer
from app.ai.ats_analyzer.service import ats_analyzer_service
from app.ai.parsers.schemas import ResumeData
from app.ai.resume_improvement.context import (
    ResumeImprovementDeterministicSignalsContext,
)
from app.models.candidate import Candidate
from app.models.job import Job


class ResumeImprovementDeterministicResult(BaseModel):
    """
    Encapsulates all deterministic and semantic signals calculated for
    the resume improvement workflow, reusing established ATS components.
    """

    ats_score: int = Field(ge=0, le=100)
    score_breakdown: ATSScoreBreakdown
    deterministic_result: ATSDeterministicResult
    semantic_relevance_score: float = Field(ge=0.0, le=1.0)
    empty_or_missing_sections: list[str] = Field(default_factory=list)
    signals_context: ResumeImprovementDeterministicSignalsContext


class ResumeImprovementAnalyzer:
    """
    Calculates deterministic signals for resume improvement.

    Reuses existing ATS deterministic skill analysis, completeness scoring,
    and semantic similarity calculation without invoking external LLMs for scoring.
    """

    def __init__(self):
        self.ats_context_builder = ats_context_builder
        self.ats_analyzer = ats_analyzer
        self.ats_semantic_analyzer = ats_semantic_analyzer
        self.ats_service = ats_analyzer_service

    def _detect_empty_or_missing_sections(
        self,
        resume_data: ResumeData,
    ) -> list[str]:
        empty_sections: list[str] = []

        if not (resume_data.summary and resume_data.summary.strip()):
            empty_sections.append("Professional Summary")

        if not resume_data.experience:
            empty_sections.append("Work Experience")

        if not resume_data.projects:
            empty_sections.append("Projects")

        if not resume_data.skills:
            empty_sections.append("Skills")

        if not resume_data.education:
            empty_sections.append("Education")

        if not resume_data.certifications:
            empty_sections.append("Certifications")

        return empty_sections

    def analyze(
        self,
        *,
        candidate: Candidate,
        candidate_skills: list[str],
        resume_data: ResumeData,
        job: Job,
        required_skills: list[str],
        preferred_skills: list[str],
    ) -> ResumeImprovementDeterministicResult:
        ats_context: ATSContext = self.ats_context_builder.build(
            first_name=candidate.first_name,
            last_name=candidate.last_name,
            headline=candidate.headline,
            bio=candidate.bio,
            location=candidate.location,
            candidate_skills=candidate_skills,
            resume_data=resume_data,
            job_title=job.title,
            job_description=job.description,
            job_location=job.location,
            employment_type=job.employment_type,
            experience_level=job.experience_level,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
        )

        deterministic_result = self.ats_analyzer.analyze(
            ats_context
        )

        semantic_relevance_score = (
            self.ats_semantic_analyzer.calculate(
                ats_context
            )
        )

        ats_score = self.ats_service._calculate_ats_score(
            required_skill_score=(
                deterministic_result.required_skill_score
            ),
            preferred_skill_score=(
                deterministic_result.preferred_skill_score
            ),
            semantic_relevance_score=(
                semantic_relevance_score
            ),
            resume_completeness_score=(
                deterministic_result.resume_completeness_score
            ),
        )

        empty_sections = self._detect_empty_or_missing_sections(
            resume_data
        )

        score_breakdown = ATSScoreBreakdown(
            required_skill_score=(
                deterministic_result.required_skill_score
            ),
            preferred_skill_score=(
                deterministic_result.preferred_skill_score
            ),
            semantic_relevance_score=(
                semantic_relevance_score
            ),
            resume_completeness_score=(
                deterministic_result.resume_completeness_score
            ),
        )

        signals_context = (
            ResumeImprovementDeterministicSignalsContext(
                ats_score=ats_score,
                required_skill_score=(
                    deterministic_result.required_skill_score
                ),
                preferred_skill_score=(
                    deterministic_result.preferred_skill_score
                ),
                semantic_relevance_score=(
                    semantic_relevance_score
                ),
                resume_completeness_score=(
                    deterministic_result.resume_completeness_score
                ),
                required_skills_matched=(
                    deterministic_result.required_skills_matched
                ),
                required_skills_missing=(
                    deterministic_result.required_skills_missing
                ),
                preferred_skills_matched=(
                    deterministic_result.preferred_skills_matched
                ),
                preferred_skills_missing=(
                    deterministic_result.preferred_skills_missing
                ),
                empty_or_missing_sections=empty_sections,
            )
        )

        return ResumeImprovementDeterministicResult(
            ats_score=ats_score,
            score_breakdown=score_breakdown,
            deterministic_result=deterministic_result,
            semantic_relevance_score=semantic_relevance_score,
            empty_or_missing_sections=empty_sections,
            signals_context=signals_context,
        )


resume_improvement_analyzer = ResumeImprovementAnalyzer()
