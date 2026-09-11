from sqlalchemy.orm import Session

from app.ai.career_coach.context import (
    CareerCoachApplicationContext,
    CareerCoachJobContext,
    career_coach_context_builder,
)
from app.ai.career_coach.prompts import career_coach_prompt_builder
from app.ai.career_coach.schemas import (
    CareerCoachRequest,
    CareerCoachResponse,
)
from app.ai.parsers.schemas import ResumeData
from app.ai.services.gemini_service import gemini_service
from app.models.candidate import Candidate
from app.services.resume import get_active_resume


class CareerCoachService:
    """
    Application service for Hirely's AI Career Coach.

    This service coordinates:
    - Candidate data retrieval
    - Resume context
    - Application/job context
    - Prompt construction
    - Gemini structured generation
    """

    def __init__(self):
        self.context_builder = career_coach_context_builder
        self.prompt_builder = career_coach_prompt_builder
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

    def _get_application_context(
        self,
        candidate: Candidate,
    ) -> list[CareerCoachApplicationContext]:
        """
        Convert candidate applications into AI-safe application context.
        """

        applications: list[CareerCoachApplicationContext] = []

        for application in candidate.applications:
            job = application.job

            if not job:
                continue

            applications.append(
                CareerCoachApplicationContext(
                    status=application.status.value,
                    job=CareerCoachJobContext(
                        title=job.title,
                        description=job.description,
                        location=job.location,
                        employment_type=job.employment_type,
                        experience_level=job.experience_level,
                    ),
                )
            )

        return applications

    def build_context(
        self,
        db: Session,
        candidate: Candidate,
    ):
        """
        Build the complete AI-safe context for a candidate.
        """

        skills = self._get_candidate_skills(candidate)
        resume_data = self._get_resume_data(db, candidate)
        applications = self._get_application_context(candidate)

        return self.context_builder.build(
            first_name=candidate.first_name,
            last_name=candidate.last_name,
            headline=candidate.headline,
            bio=candidate.bio,
            location=candidate.location,
            skills=skills,
            resume_data=resume_data,
            applications=applications,
        )

    def generate_response(
        self,
        db: Session,
        candidate: Candidate,
        request: CareerCoachRequest,
    ) -> CareerCoachResponse:
        """
        Generate a personalized Career Coach response.
        """

        context = self.build_context(
            db=db,
            candidate=candidate,
        )

        prompt = self.prompt_builder.build(
            context=context,
            message=request.message,
        )

        return self.gemini_service.generate_structured(
            prompt=prompt,
            response_schema=CareerCoachResponse,
        )


career_coach_service = CareerCoachService()