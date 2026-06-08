# app/infrastructure/database/models/latest_vital.py

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class LatestVitalModel(Base):
    """
    SQLAlchemy model for storing the latest live vital snapshot
    of a patient.

    This table keeps only one active/latest vital row per patient
    and is optimized for dashboard reads and real-time monitoring.
    """

    __tablename__ = "latest_patient_vitals"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    bed_id = Column(
        Integer,
        ForeignKey("bed_masters.id"),
        nullable=True,
        index=True,
    )

    device_id = Column(
        Integer,
        ForeignKey("device_masters.id"),
        nullable=True,
        index=True,
    )

    hr = Column(Float, nullable=True)
    bp_sys = Column(Float, nullable=True)
    bp_dia = Column(Float, nullable=True)
    spo2 = Column(Float, nullable=True)
    temp = Column(Float, nullable=True)
    rr = Column(Float, nullable=True)

    status = Column(String, nullable=True)

    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    patient = relationship("PatientModel")