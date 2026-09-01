from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SQLENUM, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.job import Job


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    SHORTLISTED = "shortlisted"
    INTERVIEW = "interview"
    HIRED = "hired"
    REJECTED = "rejected"


class Application(Base):
    __tablename__ = "applications"
    
    __table_args__ = (
        UniqueConstraint(
            "candidate_id",
            "job_id",
            name="uq_application_candidate_job",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    candidate_id: Mapped[UUID] = mapped_column(
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )

    job_id: Mapped[UUID] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=False,
        index=True,
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        SQLENUM(ApplicationStatus),
        default=ApplicationStatus.APPLIED,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    candidate: Mapped["Candidate"] = relationship(
        back_populates="applications",
    )

    job: Mapped["Job"] = relationship(
        back_populates="applications",
    )