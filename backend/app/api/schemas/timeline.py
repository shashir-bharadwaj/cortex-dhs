# app/api/schemas/timeline.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator
from app.domain.enums import TimelineEventType


class TimelineEventModelCreateRequest(BaseModel):
    """
    Request schema for creating a patient timeline event.
    """

    event: str
    type: TimelineEventType


class TimelineEventModelResponse(BaseModel):
    """
    Response schema for patient timeline events.
    """

    id: int
    time: Optional[str] = None
    event: str
    type: TimelineEventType

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def map_created_at_to_time(cls, values):
        if hasattr(values, "created_at"):
            created_at = values.created_at
            if created_at and not getattr(values, "time", None):
                values.__dict__["time"] = (
                    created_at.isoformat()
                    if isinstance(created_at, datetime)
                    else str(created_at)
                )
        return values