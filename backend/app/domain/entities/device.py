from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.enums import DeviceStatus, DeviceType

@dataclass
class Device:
    """
    Domain entity representing an ICU device.
    """

    id: Optional[int] = None
    name: str = ""
    serial_number: str = ""
    type: DeviceType = DeviceType.MONITOR
    status: DeviceStatus = DeviceStatus.OFFLINE
    last_sync: Optional[datetime] = None
    error: Optional[str] = None
    location: Optional[str] = None