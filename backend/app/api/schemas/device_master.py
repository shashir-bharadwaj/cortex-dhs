from typing import Optional

from pydantic import BaseModel, Field


class DeviceMasterCreateRequest(BaseModel):
    device_type: str = Field(..., min_length=1)
    manufacturer: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    serial: str = Field(..., min_length=1)
    bed_id: Optional[int] = Field(default=None, gt=0)
    ip_address: str = Field(..., min_length=1)
    status: str = Field(default="ACTIVE")


class DeviceMasterUpdateRequest(BaseModel):
    device_type: str = Field(..., min_length=1)
    manufacturer: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    serial: str = Field(..., min_length=1)
    bed_id: Optional[int] = Field(default=None, gt=0)
    ip_address: str = Field(..., min_length=1)
    status: str = Field(default="ACTIVE")


class DeviceMasterResponse(BaseModel):
    id: int
    device_type: str
    manufacturer: str
    model: str
    serial: str
    bed_id: Optional[int]
    ip_address: str
    status: str

    model_config = {
        "from_attributes": True
    }