from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TimelineEvent:
    """
    Domain entity representing a patient timeline event.
    """

    id: Optional[int]
    patient_id: int
    event: str
    type: str
    created_at: Optional[datetime] = None