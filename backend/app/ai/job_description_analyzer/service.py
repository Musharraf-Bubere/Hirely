from sqlalchemy.orm import Session

from app.ai.job_description_analyzer.context import (
    JobDescriptionContext,
    JobDescriptionContextBuilder,
    job_description_context_builder,
)
from app.ai.job_description_analyzer.prompts import (
    JobDescriptionPromptBuilder,
    job_description_prompt_builder,
)
from app.ai.job_description_analyzer.schemas import (
    JobDescriptionAIResult,
    JobDescriptionAnalysisResponse,
    JobDescriptionAnalysisResult,
)
from app.ai.services.gemini_service import gemini_service
from app.models.job import Job
from app.models.recruiter import Recruiter


class JobDescriptionAnalyzerService:
    """
    Orchestrates the Recruiter AI — Job Description Analyzer V1 pipeline.

    Coordinates job context building from database records, prompt generation with
    strict anti-fabrication rules, structured Gemini generation, and response assembly.
    """

    def __init__(self):
        self.context_builder: JobDescriptionContextBuilder = (
            job_description_context_builder
        )
        self.prompt_builder: JobDescriptionPromptBuilder = (
            job_description_prompt_builder
        )
        self.gemini_service = gemini_service

    def _get_job_skills(
        self,
        job: Job,
    ) -> tuple[list[str], list[str]]:
        required_skills: list[str] = []
        preferred_skills: list[str] = []

        for job_skill in job.job_skills:
            if job_skill.skill is None or not job_skill.skill.name:
                continue

            skill_name = job_skill.skill.name.strip()
            if not skill_name:
                continue

            if job_skill.is_required:
                required_skills.append(skill_name)
            else:
                preferred_skills.append(skill_name)

        return required_skills, preferred_skills

    def build_context(
        self,
        job: Job,
    ) -> JobDescriptionContext:
        required_skills, preferred_skills = self._get_job_skills(job)

        return self.context_builder.build(
            job=job,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
        )

    def analyze_job_description(
        self,
        *,
        db: Session,
        recruiter: Recruiter,
        job: Job,
    ) -> JobDescriptionAnalysisResponse:
        """
        Analyzes an existing job belonging to the authenticated recruiter.
        Advisory analysis only: does not mutate or publish the job.
        """
        if job.recruiter_id != recruiter.id:
            raise ValueError(
                "You do not have permission to analyze this job."
            )

        if not job.description or not job.description.strip():
            raise ValueError(
                "Job description cannot be empty for analysis."
            )

        context = self.build_context(job=job)

        prompt = self.prompt_builder.build(
            context=context,
        )

        ai_result: JobDescriptionAIResult = (
            self.gemini_service.generate_structured(
                prompt=prompt,
                response_schema=JobDescriptionAIResult,
            )
        )

        analysis_result = JobDescriptionAnalysisResult(
            quality_score=ai_result.quality_score,
            overall_assessment=ai_result.overall_assessment,
            strengths=ai_result.strengths,
            issues=ai_result.issues,
            missing_information=ai_result.missing_information,
            skills_analysis=ai_result.skills_analysis,
            improvement_recommendations=ai_result.improvement_recommendations,
            improved_description=ai_result.improved_description,
        )

        return JobDescriptionAnalysisResponse(
            job_id=job.id,
            analysis=analysis_result,
        )


job_description_analyzer_service = JobDescriptionAnalyzerService()
