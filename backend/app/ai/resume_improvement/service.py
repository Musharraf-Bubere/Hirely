from sqlalchemy.orm import Session

from app.ai.parsers.schemas import ResumeData
from app.ai.resume_improvement.analyzer import (
    ResumeImprovementAnalyzer,
    ResumeImprovementDeterministicResult,
    resume_improvement_analyzer,
)
from app.ai.resume_improvement.context import (
    ResumeImprovementContext,
    ResumeImprovementContextBuilder,
    resume_improvement_context_builder,
)
from app.ai.resume_improvement.prompts import (
    ResumeImprovementPromptBuilder,
    resume_improvement_prompt_builder,
)
from app.ai.resume_improvement.schemas import (
    ResumeImprovementAIResult,
    ResumeImprovementResponse,
    ResumeImprovementResult,
)
from app.ai.services.gemini_service import gemini_service
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.resume import get_active_resume


class ResumeImprovementService:
    """
    Orchestrates the Resume Improvement V1 pipeline.

    Coordinates deterministic ATS analysis, context construction with PII
    sanitization, grounded prompt building, and structured Gemini generation.
    """

    def __init__(self):
        self.context_builder: ResumeImprovementContextBuilder = (
            resume_improvement_context_builder
        )
        self.analyzer: ResumeImprovementAnalyzer = (
            resume_improvement_analyzer
        )
        self.prompt_builder: ResumeImprovementPromptBuilder = (
            resume_improvement_prompt_builder
        )
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
        *,
        db: Session,
        candidate: Candidate,
        job: Job,
    ) -> tuple[ResumeImprovementContext, ResumeImprovementDeterministicResult]:
        resume_data = self._get_resume_data(
            db=db,
            candidate=candidate,
        )

        candidate_skills = self._get_candidate_skills(
            candidate
        )

        required_skills, preferred_skills = (
            self._get_job_skills(job)
        )

        deterministic_result = self.analyzer.analyze(
            candidate=candidate,
            candidate_skills=candidate_skills,
            resume_data=resume_data,
            job=job,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
        )

        context = self.context_builder.build(
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
            deterministic_signals=deterministic_result.signals_context,
        )

        return context, deterministic_result

    def generate_improvement(
        self,
        *,
        db: Session,
        candidate: Candidate,
        job: Job,
    ) -> ResumeImprovementResponse:
        context, deterministic_result = self.build_context(
            db=db,
            candidate=candidate,
            job=job,
        )

        prompt = self.prompt_builder.build(
            context=context,
        )

        ai_result = self.gemini_service.generate_structured(
            prompt=prompt,
            response_schema=ResumeImprovementAIResult,
        )

        return ResumeImprovementResponse(
            job_id=job.id,
            resume_improvement=ResumeImprovementResult(
                overall_assessment=ai_result.overall_assessment,
                ats_score=deterministic_result.ats_score,
                score_breakdown=deterministic_result.score_breakdown,
                missing_required_skills=(
                    deterministic_result.deterministic_result.required_skills_missing
                ),
                missing_preferred_skills=(
                    deterministic_result.deterministic_result.preferred_skills_missing
                ),
                prioritized_actions=ai_result.prioritized_actions,
                required_skill_recommendations=(
                    ai_result.required_skill_recommendations
                ),
                preferred_skill_recommendations=(
                    ai_result.preferred_skill_recommendations
                ),
                section_improvements=ai_result.section_improvements,
                summary_improvements=ai_result.summary_improvements,
                experience_improvements=ai_result.experience_improvements,
                project_improvements=ai_result.project_improvements,
                skills_improvements=ai_result.skills_improvements,
            ),
        )


resume_improvement_service = ResumeImprovementService()
