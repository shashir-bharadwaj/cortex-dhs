from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class PatientStaffAssignmentModel(Base):
    """
    Staff assignment mapping between patients and users.

    Supports:
    - Assigned nurse
    - Assigned doctor
    - Care team display
    - Assignment history
    - Shift handover workflows
    """

    __tablename__ = "patient_staff_assignments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    assignment_type = Column(
        String,
        nullable=False,
        index=True,
    )
    # Examples:
    # NURSE
    # DOCTOR

    assigned_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    ended_at = Column(
        DateTime,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
    )

    patient = relationship(
        "PatientModel",
        back_populates="staff_assignments",
    )

    user = relationship(
        "UserModel",
        back_populates="staff_assignments",
    )