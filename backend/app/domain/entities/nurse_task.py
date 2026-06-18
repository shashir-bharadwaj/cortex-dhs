from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.enums.task import TaskStatus


@dataclass
class NurseTask:
    id: Optional[int] = None
    patient_id: Optional[int] = None
    patient_name: str = ""
    bed_label: str = ""
    assigned_to_id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    due_time: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
