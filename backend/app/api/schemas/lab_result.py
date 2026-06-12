from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class LabResultCreateRequest(BaseModel):
    ph: Optional[float] = None
    pao2: Optional[float] = None
    paco2: Optional[float] = None
    hco3: Optional[float] = None
    rbs: Optional[float] = None

    model_config = ConfigDict(populate_by_name=True)


class LabResultResponse(BaseModel):
    id: int
    patient_id: int = Field(alias="patientId")
    ph: Optional[float] = None
    pao2: Optional[float] = None
    paco2: Optional[float] = None
    hco3: Optional[float] = None
    rbs: Optional[float] = None
    recorded_at: Optional[datetime] = Field(default=None, alias="recordedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
