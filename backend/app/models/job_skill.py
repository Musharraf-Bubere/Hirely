from uuid import UUID

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.skill import Skill


class JobSkill(Base):
    __tablename__ = "job_skills"

    job_id: Mapped[UUID] = mapped_column(
        ForeignKey("jobs.id"),
        primary_key=True,
    )

    skill_id: Mapped[UUID] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True,
    )

    is_required: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    job: Mapped["Job"] = relationship(
        back_populates="job_skills",
    )

    skill: Mapped["Skill"] = relationship(
        back_populates="job_skills",
    )