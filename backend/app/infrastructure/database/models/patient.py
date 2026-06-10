# app/infrastructure/database/models/patient.py

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.domain.enums.patient import Gender


class PatientModel(Base):
    """
    SQLAlchemy model for ICU patients.

    Persistence representation of an admitted patient.

    Current hierarchy:
    ------------------
    Hospital -> HospitalUnit -> ICUUnitMaster -> BedMaster -> Patient
    """

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(Enum(Gender), nullable=False, default=Gender.MALE)

    bed_id = Column(
        Integer,
        ForeignKey("bed_masters.id"),
        nullable=True,
        index=True,
    )

    diagnosis = Column(String, nullable=True)

    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    blood_group = Column(String, nullable=True)
    doctor = Column(String, nullable=True)

    admission_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id"),
        nullable=False,
        index=True,
    )

    status = Column(String, nullable=False, default="admitted")

    history = Column(JSON, nullable=True, default=list)
    comorbidities = Column(JSON, nullable=True, default=list)

    vitals = relationship(
        "VitalModel",
        back_populates="patient",
        cascade="all, delete-orphan",
        order_by="desc(VitalModel.recorded_at)",
    )

    bed = relationship(
        "BedMasterModel",
    )

    hospital = relationship(
        "HospitalModel",
    )

    timeline = relationship(
        "TimelineEventModel",
        back_populates="patient",
        cascade="all, delete-orphan",
        order_by="desc(TimelineEventModel.created_at)",
    )

    staff_assignments = relationship(
        "PatientStaffAssignmentModel",
        back_populates="patient",
        cascade="all, delete-orphan",
    )