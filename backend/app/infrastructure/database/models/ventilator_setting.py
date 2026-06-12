from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class VentilatorSettingModel(Base):
    """
    Persistence model for patient ventilator parameters.
    """

    __tablename__ = "ventilator_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"), nullable=False, index=True
    )

    mode: Mapped[str] = mapped_column(String(50), nullable=True)
    fio2: Mapped[float] = mapped_column(Float, nullable=True)
    peep: Mapped[float] = mapped_column(Float, nullable=True)
    set_rr: Mapped[int] = mapped_column(Integer, nullable=True)
    tidal_volume: Mapped[float] = mapped_column(Float, nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    patient = relationship("PatientModel")
