from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class MedicationOrderModel(Base):
    """
    Persistence model for patient medication orders.
    Active infusions are medication orders with order_type=Infusion and status=Running.
    """

    __tablename__ = "medication_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patients.id"), nullable=False, index=True
    )

    drug_name: Mapped[str] = mapped_column(String(255), nullable=False)
    order_type: Mapped[str] = mapped_column(String(50), nullable=False)
    dose: Mapped[str] = mapped_column(String(100), nullable=True)
    route: Mapped[str] = mapped_column(String(50), nullable=True)
    schedule: Mapped[str] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")

    # Infusion-only fields
    rate_ml_hr: Mapped[float] = mapped_column(Float, nullable=True)
    remaining_vol_ml: Mapped[float] = mapped_column(Float, nullable=True)
    est_end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

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

    patient = relationship("PatientModel")
