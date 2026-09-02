from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.schemas.skill import SkillCreateRequest


def get_or_create_skill(
    db: Session,
    data: SkillCreateRequest,
) -> Skill:
    skill_name = data.name.strip()

    existing_skill = (
        db.query(Skill)
        .filter(
            Skill.name.ilike(skill_name),
        )
        .first()
    )

    if existing_skill:
        return existing_skill

    skill = Skill(
        name=skill_name,
    )

    db.add(skill)
    db.commit()
    db.refresh(skill)

    return skill