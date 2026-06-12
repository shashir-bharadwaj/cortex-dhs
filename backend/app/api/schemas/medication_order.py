from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums.medication import MedicationOrderType, MedicationStatus


class MedicationOrderCreateRequest(BaseModel):
    drug_name: str = Field(alias="drugName")
    order_type: MedicationOrderType = Field(alias="orderType")
    dose: Optional[str] = None
    route: Optional[str] = None
    schedule: Optional[str] = None
    status: MedicationStatus = MedicationStatus.PENDING
    rate_ml_hr: Optional[float] = Field(default=None, alias="rateMlHr")
    remaining_vol_ml: Optional[float] = Field(default=None, alias="remainingVolMl")
    est_end_time: Optional[datetime] = Field(default=None, alias="estEndTime")

    model_config = ConfigDict(populate_by_name=True)


class MedicationOrderResponse(BaseModel):
    id: int
    patient_id: int = Field(alias="patientId")
    drug_name: str = Field(alias="drugName")
    order_type: MedicationOrderType = Field(alias="orderType")
    dose: Optional[str] = None
    route: Optional[str] = None
    schedule: Optional[str] = None
    status: MedicationStatus
    rate_ml_hr: Optional[float] = Field(default=None, alias="rateMlHr")
    remaining_vol_ml: Optional[float] = Field(default=None, alias="remainingVolMl")
    est_end_time: Optional[datetime] = Field(default=None, alias="estEndTime")
    created_at: Optional[datetime] = Field(default=None, alias="createdAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
