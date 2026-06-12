from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FluidBalanceCreateRequest(BaseModel):
    in_ml: Optional[float] = Field(default=None, alias="inMl")
    out_ml: Optional[float] = Field(default=None, alias="outMl")
    source: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class FluidBalanceRecordResponse(BaseModel):
    id: int
    patient_id: int = Field(alias="patientId")
    in_ml: Optional[float] = Field(default=None, alias="inMl")
    out_ml: Optional[float] = Field(default=None, alias="outMl")
    source: Optional[str] = None
    recorded_at: Optional[datetime] = Field(default=None, alias="recordedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class FluidBalanceSummaryResponse(BaseModel):
    patient_id: int = Field(alias="patientId")
    date: str
    in_ml: float = Field(alias="inMl")
    out_ml: float = Field(alias="outMl")
    balance_ml: float = Field(alias="balanceMl")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
