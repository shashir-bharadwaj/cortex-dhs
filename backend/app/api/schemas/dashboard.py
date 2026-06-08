from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DashboardUnitResponse(BaseModel):
    id: int
    name: str
    department: Optional[str] = None
    total_beds: int = Field(alias="totalBeds")
    occupied_beds: int = Field(alias="occupiedBeds")

    model_config = ConfigDict(populate_by_name=True)


class DashboardSummaryResponse(BaseModel):
    normal: int
    warning: int
    critical: int
    active_alarms: int = Field(alias="activeAlarms")

    model_config = ConfigDict(populate_by_name=True)


class DashboardBedResponse(BaseModel):
    id: int
    bed_id: str = Field(alias="bedId")

    model_config = ConfigDict(populate_by_name=True)


class DashboardPatientResponse(BaseModel):
    id: int
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    diagnosis: Optional[str] = None
    doctor: Optional[str] = None


class DashboardVitalValueResponse(BaseModel):
    value: Optional[float | str] = None
    unit: str
    status: str
    recorded_at: Optional[datetime] = Field(default=None, alias="recordedAt")

    model_config = ConfigDict(populate_by_name=True)


class DashboardVitalsResponse(BaseModel):
    hr: Optional[DashboardVitalValueResponse] = None
    spo2: Optional[DashboardVitalValueResponse] = None
    bp: Optional[DashboardVitalValueResponse] = None
    rr: Optional[DashboardVitalValueResponse] = None
    temp: Optional[DashboardVitalValueResponse] = None


class DashboardPatientCardResponse(BaseModel):
    bed: DashboardBedResponse
    patient: Optional[DashboardPatientResponse] = None
    status: str
    vitals: Optional[DashboardVitalsResponse] = None
    monitoring: list[str] = []
    active_alarm_count: int = Field(alias="activeAlarmCount")
    has_critical_alarm: bool = Field(alias="hasCriticalAlarm")

    model_config = ConfigDict(populate_by_name=True)


class DashboardAlarmResponse(BaseModel):
    id: int
    patient_id: int = Field(alias="patientId")
    patient_name: str = Field(alias="patientName")
    bed_id: str = Field(alias="bedId")
    alarm_type: str = Field(alias="alarmType")
    device_source: str = Field(alias="deviceSource")
    message: str
    severity: str
    timestamp: datetime
    acknowledged: bool
    silenced: bool
    escalated: bool

    model_config = ConfigDict(populate_by_name=True)


class DashboardOverviewResponse(BaseModel):
    unit: DashboardUnitResponse
    summary: DashboardSummaryResponse
    patient_cards: list[DashboardPatientCardResponse] = Field(alias="patientCards")
    alarms: list[DashboardAlarmResponse]
    generated_at: datetime = Field(alias="generatedAt")

    model_config = ConfigDict(populate_by_name=True)