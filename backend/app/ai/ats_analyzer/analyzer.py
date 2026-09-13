from pydantic import BaseModel, Field

from app.ai.ats_analyzer.context import ATSContext
from app.ai.matching.skill_matching import skill_matcher


class ATSDeterministicResult(BaseModel):
    required_skill_score: float = Field(
        ge=0.0,
        le=1.0,
    )
    preferred_skill_score: float = Field(
        ge=0.0,
        le=1.0,
    )
    resume_completeness_score: float = Field(
        ge=0.0,
        le=1.0,
    )

    required_skills_matched: list[str] = Field(
        default_factory=list,
    )
    required_skills_missing: list[str] = Field(
        default_factory=list,
    )
    preferred_skills_matched: list[str] = Field(
        default_factory=list,
    )
    preferred_skills_missing: list[str] = Field(
        default_factory=list,
    )


class ATSAnalyzer:
    """
    Performs deterministic resume/job analysis.

    This component does not call an LLM. Its responsibility is to
    calculate measurable ATS signals that can be reproduced reliably.
    """

    def __init__(self):
        self.skill_matcher = skill_matcher

    def _calculate_resume_completeness(
        self,
        context: ATSContext,
    ) -> float:
        resume = context.candidate.resume

        checks = [
            bool(resume.name and resume.name.strip()),
            bool(resume.email and resume.email.strip()),
            bool(resume.phone and resume.phone.strip()),
            bool(resume.location and resume.location.strip()),
            bool(resume.headline and resume.headline.strip()),
            bool(resume.summary and resume.summary.strip()),
            bool(resume.skills),
            bool(resume.experience),
            bool(resume.projects),
            bool(resume.education),
        ]

        if not checks:
            return 0.0

        return sum(checks) / len(checks)

    def analyze(
        self,
        context: ATSContext,
    ) -> ATSDeterministicResult:
        candidate_skills = list(context.candidate.skills)

        resume_skills = [
            skill
            for skill in context.candidate.resume.skills
            if skill and skill.strip()
        ]

        combined_candidate_skills = list(
            {
                skill.strip()
                for skill in candidate_skills + resume_skills
                if skill and skill.strip()
            }
        )

        skill_result = self.skill_matcher.match(
            candidate_skills=combined_candidate_skills,
            required_skills=context.job.required_skills,
            preferred_skills=context.job.preferred_skills,
        )

        resume_completeness_score = (
            self._calculate_resume_completeness(context)
        )

        return ATSDeterministicResult(
            required_skill_score=skill_result.required_score,
            preferred_skill_score=skill_result.preferred_score,
            resume_completeness_score=resume_completeness_score,
            required_skills_matched=skill_result.required_matched,
            required_skills_missing=skill_result.required_missing,
            preferred_skills_matched=skill_result.preferred_matched,
            preferred_skills_missing=skill_result.preferred_missing,
        )


ats_analyzer = ATSAnalyzer()