from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.candidate_skill import CandidateSkill
from app.models.resume import Resume
from app.schemas.skill import SkillCreateRequest
from app.services.candidate_skill import add_candidate_skill
from app.services.skill import get_or_create_skill


def sync_resume_skills_to_candidate(
    db: Session,
    candidate: Candidate,
    resume: Resume,
) -> list[CandidateSkill]:
    if resume.candidate_id != candidate.id:
        raise ValueError("Resume does not belong to candidate")

    if not resume.parsed_data:
        raise ValueError("Resume has not been parsed")

    skills = resume.parsed_data.get("skills", [])

    if not skills:
        return []

    synchronized_skills = []

    for skill_name in skills:
        if not skill_name or not skill_name.strip():
            continue

        skill = get_or_create_skill(
            db=db,
            data=SkillCreateRequest(name=skill_name),
        )

        existing = (
            db.query(CandidateSkill)
            .filter(
                CandidateSkill.candidate_id == candidate.id,
                CandidateSkill.skill_id == skill.id,
            )
            .first()
        )

        if existing:
            synchronized_skills.append(existing)
            continue

        candidate_skill = add_candidate_skill(
            db=db,
            candidate=candidate,
            skill=skill,
        )

        synchronized_skills.append(candidate_skill)

    return synchronized_skills