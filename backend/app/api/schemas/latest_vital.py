from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class LatestVitalResponse(BaseModel):
    """
    Response schema for latest live patient vital snapshot.
    """

    id: Optional[int] = None

    patient_id: Optional[int] = Field(default=None, alias="patientId")
    bed_id: Optional[int] = Field(default=None, alias="bedId")
    device_id: Optional[int] = Field(default=None, alias="deviceId")

    hr: Optional[float] = None
    bp_sys: Optional[float] = Field(default=None, alias="bpSys")
    bp_dia: Optional[float] = Field(default=None, alias="bpDia")
    spo2: Optional[float] = None
    temp: Optional[float] = None
    rr: Optional[float] = None

    status: Optional[str] = None

    recorded_at: Optional[datetime] = Field(default=None, alias="recordedAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )