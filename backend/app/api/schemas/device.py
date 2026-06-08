from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums.device import DeviceStatus, DeviceType


class DeviceCreateRequest(BaseModel):
    """
    Request schema for creating a device.
    """

    name: str = Field(..., min_length=1)
    serial_number: str = Field(..., min_length=1)
    type: DeviceType
    status: DeviceStatus
    last_sync: Optional[datetime] = None
    error: Optional[str] = None
    location: Optional[str] = None


class DeviceUpdateRequest(BaseModel):
    """
    Request schema for updating a device.

    All fields are optional so this can support partial update behavior
    when the use case/repository applies only provided values.
    """

    name: Optional[str] = None
    serial_number: Optional[str] = None
    type: Optional[DeviceType] = None
    status: Optional[DeviceStatus] = None
    last_sync: Optional[datetime] = None
    error: Optional[str] = None
    location: Optional[str] = None


class DeviceStatusUpdateRequest(BaseModel):
    """
    Request schema for updating only device status/error.

    Used by:
        PATCH /devices/{device_id}/status
    """

    status: DeviceStatus
    error: Optional[str] = None
    last_sync: Optional[datetime] = None


class DeviceAssignRequest(BaseModel):
    """
    Request schema for assigning a device to a patient.

    Used by:
        POST /patients/{patient_id}/devices
    """

    deviceId: int = Field(..., gt=0)


class DeviceResponse(BaseModel):
    """
    Response schema for a device.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    serial_number: str
    type: DeviceType
    status: DeviceStatus
    last_sync: Optional[datetime] = None
    error: Optional[str] = None
    location: Optional[str] = None


class DeviceAssignmentResponse(BaseModel):
    """
    Response schema for device assignment.

    Field names intentionally use camelCase to match the ICU API contract.
    """

    id: int
    patientId: int
    deviceId: int
    assignedAt: datetime
    removedAt: Optional[datetime] = None
    device: Optional[DeviceResponse] = None