from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums.task import TaskStatus


class NurseTaskCreateRequest(BaseModel):
    patient_id: int = Field(alias="patientId")
    title: str
    description: Optional[str] = None
    due_time: Optional[datetime] = Field(default=None, alias="dueTime")
    assigned_to_id: Optional[int] = Field(default=None, alias="assignedToId")

    model_config = ConfigDict(populate_by_name=True)


class NurseTaskResponse(BaseModel):
    id: int
    patient_id: int = Field(alias="patientId")
    patient_name: str = Field(alias="patientName")
    bed_label: str = Field(alias="bedLabel")
    assigned_to_id: Optional[int] = Field(default=None, alias="assignedToId")
    title: str
    description: Optional[str] = None
    due_time: Optional[datetime] = Field(default=None, alias="dueTime")
    status: TaskStatus
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    completed_at: Optional[datetime] = Field(default=None, alias="completedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class NurseTaskSummaryResponse(BaseModel):
    total: int
    pending: int
    in_progress: int = Field(alias="inProgress")
    completed: int
    tasks: list[NurseTaskResponse]

    model_config = ConfigDict(populate_by_name=True)
