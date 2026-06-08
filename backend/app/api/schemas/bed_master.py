from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BedMasterCreateRequest(BaseModel):
    bed_id: str = Field(..., min_length=1)
    icu_unit_id: int = Field(..., gt=0)
    bed_type: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    ward: str = Field(..., min_length=1)
    floor: str = Field(..., min_length=1)
    room: str = Field(..., min_length=1)
    cleaning_status: str = Field(..., min_length=1)
    maintenance_status: str = Field(..., min_length=1)
    operational_status: str = Field(..., min_length=1)
    last_sanitized: Optional[datetime] = None


class BedMasterUpdateRequest(BaseModel):
    bed_id: str = Field(..., min_length=1)
    icu_unit_id: int = Field(..., gt=0)
    bed_type: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    ward: str = Field(..., min_length=1)
    floor: str = Field(..., min_length=1)
    room: str = Field(..., min_length=1)
    cleaning_status: str = Field(..., min_length=1)
    maintenance_status: str = Field(..., min_length=1)
    operational_status: str = Field(..., min_length=1)
    last_sanitized: Optional[datetime] = None


class BedMasterResponse(BaseModel):
    id: int
    bed_id: str
    icu_unit_id: int
    bed_type: str
    department: str
    ward: str
    floor: str
    room: str
    cleaning_status: str
    maintenance_status: str
    operational_status: str
    last_sanitized: Optional[datetime]

    model_config = {
        "from_attributes": True
    }