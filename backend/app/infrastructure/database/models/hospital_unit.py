from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class HospitalUnitModel(Base):
    """
    SQLAlchemy model for hospital units.

    Business role:
    --------------
    Represents a public-facing ICU/unit within a hospital.
    """

    __tablename__ = "hospital_units"
    __table_args__ = (
        UniqueConstraint("hospital_id", "name", name="uq_hospital_units_hospital_id_name"),
    )

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String(255), nullable=False)
    code = Column(String(100), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    hospital = relationship(
        "HospitalModel",
        back_populates="units",
    )