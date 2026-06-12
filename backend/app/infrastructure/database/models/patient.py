# app/infrastructure/database/models/patient.py

from datetime import datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.domain.enums.patient import Gender


class PatientModel(Base):
    """
    SQLAlchemy model for ICU patients.

    Current implementation represents an active
    patient admission/encounter.

    Future hierarchy:

    Patient (MRN/UHID)
        └── Encounters (CR Number)
                └── ICU Stay
    """

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Patient identifiers
    # ---------------------------------------------------------

    mrn = Column(
        String(100),
        nullable=False,
        index=True,        
    )

    cr_number = Column(
        String(100),
        nullable=False,
        index=True,
        unique=True,
    )

    contact_number = Column(
        String(20),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Demographics
    # ---------------------------------------------------------

    name = Column(
        String,
        nullable=False,
    )

    age = Column(
        Integer,
        nullable=True,
    )

    gender = Column(
        Enum(Gender),
        nullable=False,
        default=Gender.MALE,
    )

    blood_group = Column(
        String,
        nullable=True,
    )

    weight = Column(
        Float,
        nullable=True,
    )

    height = Column(
        Float,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Admission details
    # ---------------------------------------------------------

    bed_id = Column(
        Integer,
        ForeignKey("bed_masters.id"),
        nullable=True,
        index=True,
    )

    diagnosis = Column(
        String,
        nullable=True,
    )

    doctor = Column(
        String,
        nullable=True,
    )

    admission_time = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id"),
        nullable=False,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        default="admitted",
    )

    # ---------------------------------------------------------
    # Clinical context
    # ---------------------------------------------------------

    history = Column(
        JSON,
        nullable=True,
        default=list,
    )

    comorbidities = Column(
        JSON,
        nullable=True,
        default=list,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

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

    clinical_notes = relationship(
        "ClinicalNoteModel",
        back_populates="patient",
        cascade="all, delete-orphan",
        order_by="desc(ClinicalNoteModel.created_at)",
    )