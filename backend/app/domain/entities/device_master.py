from dataclasses import dataclass
from typing import Optional


@dataclass
class DeviceMaster:
    """
    Domain entity representing an admin-managed device registration.

    Business mapping:
    - A device may be mapped to one bed.
    - If mapped, patient-device relation can be derived through:
      patient -> bed -> device.
    """

    id: Optional[int]
    device_type: str
    manufacturer: str
    model: str
    serial: str
    bed_id: Optional[int]
    ip_address: str
    status: str