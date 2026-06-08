from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.database import Base


class AlarmModel(Base):
    """
    SQLAlchemy model for ICU patient/device alarms.
    """

    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    patient_id = Column(Integer, nullable=False, index=True)
    patient_name = Column(String, nullable=False)
    bed_id = Column(String, nullable=False)
    device = Column(String, nullable=False)

    message = Column(String, nullable=False)
    severity = Column(String, nullable=False, index=True)

    acknowledged = Column(Boolean, nullable=False, default=False)
    silenced = Column(Boolean, nullable=False, default=False)
    escalated = Column(Boolean, nullable=False, default=False)

    acknowledged_by = Column(String, nullable=True)
    silenced_by = Column(String, nullable=True)
    silence_until = Column(DateTime, nullable=True)

    escalated_by = Column(String, nullable=True)
    escalate_to = Column(String, nullable=True)