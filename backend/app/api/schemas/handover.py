from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class HandoverVitals(BaseModel):
    hr: Optional[float] = None
    spo2: Optional[float] = None
    bp: Optional[str] = None
    rr: Optional[float] = None
    temp: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True)


class HandoverNote(BaseModel):
    text: str
    author: str

    model_config = ConfigDict(populate_by_name=True)


class HandoverPatientCard(BaseModel):
    patient_id: int = Field(alias="patientId")
    bed_label: str = Field(alias="bedLabel")
    patient_name: str = Field(alias="patientName")
    age: Optional[int] = None
    gender: Optional[str] = None
    diagnosis: Optional[str] = None
    vitals: HandoverVitals
    doctor: Optional[str] = None
    unacknowledged_alarms: int = Field(alias="unacknowledgedAlarms")
    pending_tasks: int = Field(alias="pendingTasks")
    latest_note: Optional[HandoverNote] = Field(default=None, alias="latestNote")
    ventilator_active: bool = Field(alias="ventilatorActive")

    model_config = ConfigDict(populate_by_name=True)


class ShiftInfo(BaseModel):
    name: str
    start: str
    end: str

    model_config = ConfigDict(populate_by_name=True)


class ShiftHandoverResponse(BaseModel):
    shift: ShiftInfo
    patients: List[HandoverPatientCard]

    model_config = ConfigDict(populate_by_name=True)
