from sqlalchemy.orm import Session

from app.ai.ats_analyzer.analyzer import (
    ats_analyzer,
)
from app.ai.ats_analyzer.context import (
    ats_context_builder,
)
from app.ai.ats_analyzer.prompts import (
    ats_prompt_builder,
)
from app.ai.ats_analyzer.schemas import (
    ATSAnalysisResponse,
    ATSAnalysisResult,
    ATSScoreBreakdown,
)
from app.ai.ats_analyzer.semantic import (
    ats_semantic_analyzer,
)
from app.ai.parsers.schemas import ResumeData
from app.ai.services.gemini_service import gemini_service
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.resume import get_active_resume


class ATSAnalyzerService:
    """
    Orchestrates the complete ATS analysis workflow.

    Deterministic calculations and semantic similarity are performed
    separately from LLM-based qualitative analysis.
    """

    def __init__(self):
        self.context_builder = ats_context_builder
        self.analyzer = ats_analyzer
        self.semantic_analyzer = ats_semantic_analyzer
        self.prompt_builder = ats_prompt_builder
        self.gemini_service = gemini_service

    def _get_candidate_skills(
        self,
        candidate: Candidate,
    ) -> list[str]:
        return [
            candidate_skill.skill.name
            for candidate_skill in candidate.candidate_skills
            if candidate_skill.skill is not None
            and candidate_skill.skill.name
        ]

    def _get_resume_data(
        self,
        db: Session,
        candidate: Candidate,
    ) -> ResumeData:
        resume = get_active_resume(
            db,
            candidate,
        )

        if not resume:
            raise ValueError(
                "Candidate does not have an active resume."
            )

        if resume.parsing_status != "COMPLETED":
            raise ValueError(
                "Candidate's active resume has not been parsed successfully."
            )

        if not resume.parsed_data:
            raise ValueError(
                "Candidate's active resume does not contain parsed data."
            )

        return ResumeData.model_validate(
            resume.parsed_data
        )

    def _get_job_skills(
        self,
        job: Job,
    ) -> tuple[list[str], list[str]]:
        required_skills: list[str] = []
        preferred_skills: list[str] = []

        for job_skill in job.job_skills:
            if job_skill.skill is None:
                continue

            skill_name = job_skill.skill.name

            if not skill_name or not skill_name.strip():
                continue

            if job_skill.is_required:
                required_skills.append(skill_name)
            else:
                preferred_skills.append(skill_name)

        return required_skills, preferred_skills

    def build_context(
        self,
        db: Session,
        candidate: Candidate,
        job: Job,
    ):
        candidate_skills = self._get_candidate_skills(
            candidate
        )

        resume_data = self._get_resume_data(
            db,
            candidate,
        )

        required_skills, preferred_skills = (
            self._get_job_skills(job)
        )

        return self.context_builder.build(
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

    def _calculate_ats_score(
        self,
        *,
        required_skill_score: float,
        preferred_skill_score: float,
        semantic_relevance_score: float,
        resume_completeness_score: float,
    ) -> int:
        """
        Calculate the final ATS score using deterministic signals.

        Required skill coverage receives the highest weight because
        required qualifications are the strongest job-specific signal.
        """

        weighted_score = (
            required_skill_score * 0.45
            + preferred_skill_score * 0.15
            + semantic_relevance_score * 0.30
            + resume_completeness_score * 0.10
        )

        return round(weighted_score * 100)

    def generate_analysis(
        self,
        *,
        db: Session,
        candidate: Candidate,
        job: Job,
    ) -> ATSAnalysisResponse:
        context = self.build_context(
            db=db,
            candidate=candidate,
            job=job,
        )

        deterministic_result = self.analyzer.analyze(
            context
        )

        semantic_relevance_score = (
            self.semantic_analyzer.calculate(
                context
            )
        )

        ats_score = self._calculate_ats_score(
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

        prompt = self.prompt_builder.build(
            context=context,
        )

        ai_result = self.gemini_service.generate_structured(
            prompt=prompt,
            response_schema=ATSAnalysisResult,
        )

        return ATSAnalysisResponse(
            job_id=job.id,
            ats_analysis=ATSAnalysisResult(
                ats_score=ats_score,
                score_breakdown=ATSScoreBreakdown(
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
                strengths=ai_result.strengths,
                improvement_areas=ai_result.improvement_areas,
                suggestions=ai_result.suggestions,
                summary=ai_result.summary,
            ),
        )


ats_analyzer_service = ATSAnalyzerService()