from datetime import UTC, datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.domain.enums.clinical_note import ClinicalNoteType


class ClinicalNoteModel(Base):
    """
    Persistence model for patient clinical notes.
    """

    __tablename__ = "clinical_notes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"),
        nullable=False,
        index=True,
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    author_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    note_type: Mapped[ClinicalNoteType] = mapped_column(
        Enum(
            ClinicalNoteType,
            values_callable=lambda enum: [
                item.value for item in enum
            ],
            name="clinicalnotetype",
        ),
        nullable=False,
        default=ClinicalNoteType.PROGRESS,
    )

    note_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    patient = relationship(
        "PatientModel",
    )

    author = relationship(
        "UserModel",
    )