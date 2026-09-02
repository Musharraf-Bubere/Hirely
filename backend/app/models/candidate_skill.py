from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.skill import Skill


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    candidate_id: Mapped[UUID] = mapped_column(
        ForeignKey("candidates.id"),
        primary_key=True,
    )

    skill_id: Mapped[UUID] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True,
    )

    candidate: Mapped["Candidate"] = relationship(
        back_populates="candidate_skills",
    )

    skill: Mapped["Skill"] = relationship(
        back_populates="candidate_skills",
    )