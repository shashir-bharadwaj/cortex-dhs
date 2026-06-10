# app/api/schemas/vitals.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VitalCreateRequest(BaseModel):
    """
    Request schema used when creating a new vital entry
    for a specific patient.
    """

    hr: Optional[float] = Field(
        default=None,
        description="Heart rate in beats per minute",
        example=90,
    )
    bp_sys: Optional[float] = Field(
        default=None,
        description="Systolic blood pressure",
        example=120,
        alias="bpSys",
    )
    bp_dia: Optional[float] = Field(
        default=None,
        description="Diastolic blood pressure",
        example=80,
        alias="bpDia",
    )
    spo2: Optional[float] = Field(
        default=None,
        description="Oxygen saturation percentage",
        example=98,
    )
    temp: Optional[float] = Field(
        default=None,
        description="Body temperature in Fahrenheit",
        example=98.9,
    )
    rr: Optional[float] = Field(
        default=None,
        description="Respiratory rate per minute",
        example=18,
    )
    recorded_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the vital was recorded",
        example="2026-04-13T10:00:00",
        alias="recordedAt",
    )

    model_config = ConfigDict(populate_by_name=True)


class VitalResponse(BaseModel):
    """
    Response schema returned to API consumers
    after creating/fetching vitals.
    """

    id: int
    patient_id: int = Field(alias="patientId")

    hr: Optional[float] = None
    bp_sys: Optional[float] = Field(default=None, alias="bpSys")
    bp_dia: Optional[float] = Field(default=None, alias="bpDia")
    spo2: Optional[float] = None
    temp: Optional[float] = None
    rr: Optional[float] = None
    recorded_at: Optional[datetime] = Field(default=None, alias="recordedAt")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )