from typing import Optional

from pydantic import BaseModel, Field


class ICUUnitMasterCreateRequest(BaseModel):
    icu_name: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    beds: int = Field(..., ge=1)
    devices: Optional[str] = None
    gateway: Optional[str] = None
    status: str = Field(default="ACTIVE")


class ICUUnitMasterUpdateRequest(BaseModel):
    icu_name: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    beds: int = Field(..., ge=1)
    devices: Optional[str] = None
    gateway: Optional[str] = None
    status: str = Field(default="ACTIVE")


class ICUUnitMasterResponse(BaseModel):
    id: int
    icu_name: str
    type: str
    department: str
    beds: int
    devices: Optional[str]
    gateway: Optional[str]
    status: str

    model_config = {
        "from_attributes": True
    }