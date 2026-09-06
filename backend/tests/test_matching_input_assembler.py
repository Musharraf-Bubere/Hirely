from uuid import UUID

from app.ai.representations.candidate import CandidateRepresentation
from app.ai.representations.job import JobRepresentation
from app.ai.services.candidate_preparation_service import (
    CandidatePreparationResult,
)
from app.ai.services.job_preparation_service import (
    JobPreparationResult,
)
from app.ai.services.matching_input_assembler import (
    MatchingInputAssembler,
    MatchingInputAssembly,
)


def test_matching_input_assembler_builds_matching_input():
    candidate_id = UUID("11111111-1111-1111-1111-111111111111")
    job_id = UUID("22222222-2222-2222-2222-222222222222")

    candidate_preparation = CandidatePreparationResult(
        candidate_id=candidate_id,
        representation=CandidateRepresentation(
            profile_text="Candidate Profile"
        ),
        embedding=[0.1, 0.2, 0.3],
    )

    job_preparation = JobPreparationResult(
        job_id=job_id,
        representation=JobRepresentation(
            job_text="Job Profile"
        ),
        embedding=[0.4, 0.5, 0.6],
    )

    data = MatchingInputAssembly(
        candidate_preparation=candidate_preparation,
        candidate_skills=["Python", "FastAPI"],
        job_preparation=job_preparation,
        required_skills=["Python", "Docker"],
        preferred_skills=["AWS"],
    )

    assembler = MatchingInputAssembler()

    result = assembler.assemble(data)

    assert result.candidate_id == candidate_id
    assert result.candidate_skills == ["Python", "FastAPI"]
    assert result.required_skills == ["Python", "Docker"]
    assert result.preferred_skills == ["AWS"]
    assert result.candidate_embedding == [0.1, 0.2, 0.3]
    assert result.job_embedding == [0.4, 0.5, 0.6]