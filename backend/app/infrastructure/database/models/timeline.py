from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.domain.enums.timeline import TimelineEventType


class TimelineEventModel(Base):
    """
    SQLAlchemy model for patient timeline events.
    """

    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    type = Column(Enum(TimelineEventType), nullable=False)
    event = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    patient = relationship("PatientModel", back_populates="timeline")