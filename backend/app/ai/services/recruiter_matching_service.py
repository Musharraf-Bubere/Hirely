from sqlalchemy.orm import Session

from app.ai.matching.inputs import MatchingInput
from app.ai.matching.results import (
    FinalMatchResult,
    RankedMatchResult,
)
from app.ai.parsers.schemas import ResumeData
from app.ai.services.candidate_preparation_service import (
    CandidatePreparationInput,
    CandidatePreparationService,
)
from app.ai.services.job_preparation_service import (
    JobPreparationInput,
    JobPreparationService,
)
from app.ai.services.matching_input_assembler import (
    MatchingInputAssembler,
    MatchingInputAssembly,
)
from app.ai.services.matching_orchestrator import (
    ExplanationRequest,
    MatchingOrchestrator,
)
from app.ai.embeddings.service import embedding_service
from app.ai.matching.engine import matching_engine
from app.ai.representations.candidate import (
    candidate_representation_builder,
)
from app.ai.representations.job import (
    job_representation_builder,
)
from app.ai.services.match_explanation_service import (
    match_explanation_service,
)
from app.ai.services.matching_service import matching_service
from app.models.job import Job
from app.services.candidate import get_candidates
from app.services.candidate_skill import get_candidate_skills
from app.services.job_skill import get_job_skills
from app.services.resume import get_active_resume


class RecruiterMatchingService:
    """
    Coordinates the recruiter-side candidate matching workflow.

    Responsibilities:
    - Prepare the job once.
    - Find eligible candidates.
    - Prepare candidate representations and embeddings.
    - Assemble matching inputs.
    - Calculate candidate-job matches.
    - Rank candidates.
    - Optionally generate AI explanations for top-ranked candidates.
    """

    def __init__(
        self,
        candidate_preparation_service: CandidatePreparationService,
        job_preparation_service: JobPreparationService,
        matching_input_assembler: MatchingInputAssembler,
        matching_orchestrator: MatchingOrchestrator,
    ):
        self.candidate_preparation_service = (
            candidate_preparation_service
        )
        self.job_preparation_service = (
            job_preparation_service
        )
        self.matching_input_assembler = matching_input_assembler
        self.matching_orchestrator = matching_orchestrator

    def _prepare_job(
        self,
        job: Job,
        required_skills: list[str],
        preferred_skills: list[str],
    ):
        """
        Prepare the job representation and embedding once.

        The same prepared job is reused for every candidate.
        """

        return self.job_preparation_service.prepare(
            JobPreparationInput(
                job_id=job.id,
                title=job.title,
                description=job.description,
                location=job.location,
                employment_type=job.employment_type,
                experience_level=job.experience_level,
                required_skills=required_skills,
                preferred_skills=preferred_skills,
            )
        )

    def _prepare_candidate_inputs(
        self,
        db: Session,
        job_preparation,
        required_skills: list[str],
        preferred_skills: list[str],
    ) -> list[MatchingInput]:
        """
        Prepare all eligible candidates for matching.

        A candidate is eligible when:
        - They have an active resume.
        - Their resume parsing is completed.
        - Parsed resume data exists.
        - Parsed resume data passes ResumeData validation.
        """

        candidates = get_candidates(db=db)

        matching_inputs: list[MatchingInput] = []

        for candidate in candidates:
            resume = get_active_resume(
                db=db,
                candidate=candidate,
            )

            if not resume:
                continue

            if resume.parsing_status != "COMPLETED":
                continue

            if not resume.parsed_data:
                continue

            try:
                resume_data = ResumeData.model_validate(
                    resume.parsed_data
                )
            except Exception:
                continue

            candidate_skills = get_candidate_skills(
                db=db,
                candidate=candidate,
            )

            candidate_preparation = (
                self.candidate_preparation_service.prepare(
                    CandidatePreparationInput(
                        candidate_id=candidate.id,
                        resume_data=resume_data,
                    )
                )
            )

            matching_input = self.matching_input_assembler.assemble(
                MatchingInputAssembly(
                    candidate_preparation=candidate_preparation,
                    candidate_skills=candidate_skills,
                    job_preparation=job_preparation,
                    required_skills=required_skills,
                    preferred_skills=preferred_skills,
                )
            )

            matching_inputs.append(matching_input)

        return matching_inputs

    def rank_candidates(
        self,
        db: Session,
        job: Job,
    ) -> list[RankedMatchResult]:
        """
        Run the complete recruiter candidate-ranking workflow.

        Workflow:

        Job
          ↓
        Job Preparation
          ↓
        Eligible Candidates
          ↓
        Candidate Preparation
          ↓
        Matching
          ↓
        Ranking
          ↓
        RankedMatchResult[]
        """

        required_skills, preferred_skills = get_job_skills(
            db=db,
            job=job,
        )

        job_preparation = self._prepare_job(
            job=job,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
        )

        matching_inputs = self._prepare_candidate_inputs(
            db=db,
            job_preparation=job_preparation,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
        )

        if not matching_inputs:
            return []

        matching_results = [
            self.matching_orchestrator.match(
                matching_input
            )
            for matching_input in matching_inputs
        ]

        return self.matching_orchestrator.rank_match_results(
            matching_results
        )

    def explain_ranked_candidates(
        self,
        ranked_results: list[RankedMatchResult],
        explanation_limit: int,
    ) -> list[FinalMatchResult]:
        """
        Generate AI explanations for the top-ranked candidates.

        Only the top N candidates receive explanations.
        Remaining candidates keep explanation=None.

        This prevents unnecessary Gemini calls for every candidate.
        """

        explanation_request = ExplanationRequest(
            ranked_matches=ranked_results,
            explanation_limit=explanation_limit,
        )

        return self.matching_orchestrator.explain_ranked_matches(
            explanation_request
        )

    def rank_and_explain_candidates(
        self,
        db: Session,
        job: Job,
        explanation_limit: int,
    ) -> list[FinalMatchResult]:
        """
        Run candidate ranking followed by optional AI explanations.

        Workflow:

        Job
          ↓
        Prepare Job
          ↓
        Prepare Eligible Candidates
          ↓
        Match
          ↓
        Rank
          ↓
        Select Top N
          ↓
        Gemini Explanation
          ↓
        FinalMatchResult[]
        """

        ranked_results = self.rank_candidates(
            db=db,
            job=job,
        )

        if not ranked_results:
            return []

        return self.explain_ranked_candidates(
            ranked_results=ranked_results,
            explanation_limit=explanation_limit,
        )


# ---------------------------------------------------------------------------
# Shared AI service dependencies
# ---------------------------------------------------------------------------
#
# These are created once and injected into RecruiterMatchingService.
# This keeps the recruiter matching workflow consistent with the existing
# matching architecture used elsewhere in Hirely.
#

candidate_preparation_service = CandidatePreparationService(
    representation_builder=candidate_representation_builder,
    embedding_service=embedding_service,
)

job_preparation_service = JobPreparationService(
    representation_builder=job_representation_builder,
    embedding_service=embedding_service,
)

matching_input_assembler = MatchingInputAssembler()

matching_orchestrator = MatchingOrchestrator(
    matching_engine=matching_engine,
    matching_service=matching_service,
    match_explanation_service=match_explanation_service,
)

recruiter_matching_service = RecruiterMatchingService(
    candidate_preparation_service=candidate_preparation_service,
    job_preparation_service=job_preparation_service,
    matching_input_assembler=matching_input_assembler,
    matching_orchestrator=matching_orchestrator,
)