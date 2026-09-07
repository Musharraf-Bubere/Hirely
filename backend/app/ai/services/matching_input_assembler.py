from pydantic import BaseModel

from app.ai.matching.inputs import MatchingInput
from app.ai.services.job_preparation_service import JobPreparationResult
from app.ai.services.candidate_preparation_service import CandidatePreparationResult


class MatchingInputAssembly(BaseModel):
    candidate_preparation: CandidatePreparationResult
    candidate_skills: list[str]
    job_preparation: JobPreparationResult
    required_skills: list[str]
    preferred_skills: list[str] = []


class MatchingInputAssembler:
    def assemble(
        self,
        data: MatchingInputAssembly,
    ) -> MatchingInput:
        return MatchingInput(
            candidate_id=data.candidate_preparation.candidate_id,
            candidate_skills=data.candidate_skills,
            required_skills=data.required_skills,
            preferred_skills=data.preferred_skills,
            candidate_embedding=data.candidate_preparation.embedding,
            job_embedding=data.job_preparation.embedding,
        )