from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VentilatorSettingCreateRequest(BaseModel):
    mode: Optional[str] = None
    fio2: Optional[float] = None
    peep: Optional[float] = None
    set_rr: Optional[int] = Field(default=None, alias="setRr")
    tidal_volume: Optional[float] = Field(default=None, alias="tidalVolume")

    model_config = ConfigDict(populate_by_name=True)


class VentilatorSettingResponse(BaseModel):
    id: int
    patient_id: int = Field(alias="patientId")
    mode: Optional[str] = None
    fio2: Optional[float] = None
    peep: Optional[float] = None
    set_rr: Optional[int] = Field(default=None, alias="setRr")
    tidal_volume: Optional[float] = Field(default=None, alias="tidalVolume")
    recorded_at: Optional[datetime] = Field(default=None, alias="recordedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
