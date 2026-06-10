from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.domain.enums.alarm import AlarmSeverity



class AlarmCreateRequest(BaseModel):
    patient_id: int = Field(..., alias="patientId")
    patient_name: str = Field(..., alias="patientName")
    bed_id: str = Field(..., alias="bedId")
    device: str
    message: str
    severity: AlarmSeverity

    model_config = ConfigDict(from_attributes=True,)


class AlarmResponse(BaseModel):
    id: int
    timestamp: datetime

    patient_id: int = Field(..., alias="patientId")
    patient_name: str = Field(..., alias="patientName")
    bed_id: str = Field(..., alias="bedId")
    device: str

    message: str
    severity: AlarmSeverity

    acknowledged: bool
    silenced: bool
    escalated: bool

    acknowledged_by: str | None = Field(None, alias="acknowledgedBy")
    silenced_by: str | None = Field(None, alias="silencedBy")
    silence_until: datetime | None = Field(None, alias="silenceUntil")

    escalated_by: str | None = Field(None, alias="escalatedBy")
    escalate_to: str | None = Field(None, alias="escalateTo")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class AcknowledgeAlarmRequest(BaseModel):
    acknowledged_by: str = Field(..., alias="acknowledgedBy")

    model_config = ConfigDict(populate_by_name=True)


class SilenceAlarmRequest(BaseModel):
    silenced_by: str = Field(..., alias="silencedBy")
    duration_minutes: int = Field(..., alias="durationMinutes")

    model_config = ConfigDict(populate_by_name=True)

class EscalateAlarmRequest(BaseModel):
    escalated_by: str = Field(..., alias="escalatedBy")
    escalate_to: str = Field(..., alias="escalateTo")

    model_config = ConfigDict(populate_by_name=True)