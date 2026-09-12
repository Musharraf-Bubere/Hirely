from sqlalchemy.orm import Session

from app.ai.cover_letter.context import (
    CoverLetterContext,
    cover_letter_context_builder,
)
from app.ai.cover_letter.prompts import cover_letter_prompt_builder
from app.ai.cover_letter.schemas import CoverLetterResponse
from app.ai.parsers.schemas import ResumeData
from app.ai.services.gemini_service import gemini_service
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.resume import get_active_resume


class CoverLetterService:
    """
    Application service for Hirely's AI Cover Letter Generator.

    This service coordinates:
    - Candidate profile data
    - Candidate skills
    - Active resume data
    - Target job data
    - Job skill requirements
    - Prompt construction
    - Gemini structured generation
    """

    def __init__(self):
        self.context_builder = cover_letter_context_builder
        self.prompt_builder = cover_letter_prompt_builder
        self.gemini_service = gemini_service

    def _get_candidate_skills(
        self,
        candidate: Candidate,
    ) -> list[str]:
        """
        Extract skill names from the candidate's skill relationships.
        """

        return [
            candidate_skill.skill.name
            for candidate_skill in candidate.candidate_skills
            if candidate_skill.skill is not None
        ]

    def _get_resume_data(
        self,
        db: Session,
        candidate: Candidate,
    ) -> ResumeData | None:
        """
        Retrieve parsed data from the candidate's active resume.

        If no active resume exists or the resume has not been parsed,
        return None.
        """

        resume = get_active_resume(db, candidate)

        if not resume or not resume.parsed_data:
            return None

        return ResumeData.model_validate(resume.parsed_data)

    def _get_job_skills(
        self,
        job: Job,
    ) -> tuple[list[str], list[str]]:
        """
        Extract required and preferred skill names from the job.
        """

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
    ) -> CoverLetterContext:
        """
        Build the complete AI-safe candidate + job context.
        """

        candidate_skills = self._get_candidate_skills(candidate)

        resume_data = self._get_resume_data(
            db=db,
            candidate=candidate,
        )

        required_skills, preferred_skills = self._get_job_skills(job)

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

    def generate_cover_letter(
        self,
        db: Session,
        candidate: Candidate,
        job: Job,
    ) -> CoverLetterResponse:
        """
        Generate a personalized cover letter for a specific job.
        """

        context = self.build_context(
            db=db,
            candidate=candidate,
            job=job,
        )

        prompt = self.prompt_builder.build(
            context=context,
        )

        return self.gemini_service.generate_structured(
            prompt=prompt,
            response_schema=CoverLetterResponse,
        )


cover_letter_service = CoverLetterService()