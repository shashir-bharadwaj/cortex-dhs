from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class IngestionSourceSchema(BaseModel):
    hospital_id: Optional[str] = None
    unit_id: Optional[str] = None
    bed_id: str
    device_id: Optional[str] = None
    device_type: Optional[str] = None


class IngestionPatientSchema(BaseModel):
    patient_id: Optional[str] = None


class IngestionMetricSchema(BaseModel):
    code: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None


class IngestionEventSchema(BaseModel):
    event_type: str = Field(..., examples=["measurement", "alarm"])
    event_time: Optional[datetime] = None
    timestamp: Optional[datetime] = None

    source: IngestionSourceSchema
    patient: Optional[IngestionPatientSchema] = None
    metric: Optional[IngestionMetricSchema] = None

    severity: Optional[str] = None
    message: Optional[str] = None
    alarm: Optional[str] = None

    raw: Optional[dict[str, Any]] = None


class IngestDeviceEventsRequest(BaseModel):
    events: List[IngestionEventSchema]


class IngestDeviceEventsResponse(BaseModel):
    received: int
    processed: int
    vitals_created: int
    alarms_created: int
    failed: int