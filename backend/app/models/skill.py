from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.candidate_skill import CandidateSkill
    from app.models.job_skill import JobSkill


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    candidate_skills: Mapped[list["CandidateSkill"]] = relationship(
        back_populates="skill",
    )

    job_skills: Mapped[list["JobSkill"]] = relationship(
        back_populates="skill",
    )