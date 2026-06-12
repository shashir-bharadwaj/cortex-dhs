from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class LabResultModel(Base):
    """
    Persistence model for patient lab results (ABG + RBS).
    """

    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"), nullable=False, index=True
    )

    ph: Mapped[float] = mapped_column(Float, nullable=True)
    pao2: Mapped[float] = mapped_column(Float, nullable=True)
    paco2: Mapped[float] = mapped_column(Float, nullable=True)
    hco3: Mapped[float] = mapped_column(Float, nullable=True)
    rbs: Mapped[float] = mapped_column(Float, nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    patient = relationship("PatientModel")
