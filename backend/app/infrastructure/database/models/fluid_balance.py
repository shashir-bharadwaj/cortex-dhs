from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class FluidBalanceModel(Base):
    """
    Persistence model for patient fluid intake/output records.
    """

    __tablename__ = "fluid_balance_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"), nullable=False, index=True
    )

    in_ml: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    out_ml: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    source: Mapped[str] = mapped_column(String(100), nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    patient = relationship("PatientModel")
