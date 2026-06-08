# app/api/schemas/timeline.py

from typing import Literal

from pydantic import BaseModel, ConfigDict
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
    time: str
    event: str
    type: TimelineEventType

    model_config = ConfigDict(from_attributes=True)