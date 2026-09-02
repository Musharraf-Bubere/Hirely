from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.candidate_skill import CandidateSkill
from app.models.skill import Skill


def add_candidate_skill(
    db: Session,
    candidate: Candidate,
    skill: Skill,
) -> CandidateSkill:
    existing = (
        db.query(CandidateSkill)
        .filter(
            CandidateSkill.candidate_id == candidate.id,
            CandidateSkill.skill_id == skill.id,
        )
        .first()
    )

    if existing:
        raise ValueError("Skill already added to candidate")

    candidate_skill = CandidateSkill(
        candidate_id=candidate.id,
        skill_id=skill.id,
    )

    db.add(candidate_skill)
    db.commit()
    db.refresh(candidate_skill)

    return candidate_skill