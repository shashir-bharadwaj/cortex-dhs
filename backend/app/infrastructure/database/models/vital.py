from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class VitalModel(Base):
    """
    SQLAlchemy model for storing patient vital records.
    """

    __tablename__ = "vitals"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True,
    )

    hr = Column(Float, nullable=True)
    bp_sys = Column(Float, nullable=True)
    bp_dia = Column(Float, nullable=True)
    spo2 = Column(Float, nullable=True)
    temp = Column(Float, nullable=True)
    rr = Column(Float, nullable=True)

    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    patient = relationship("PatientModel", back_populates="vitals")