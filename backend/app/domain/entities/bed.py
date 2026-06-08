from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BedMaster:
    """
    Domain entity representing a hospital bed managed by admin users.

    Business mapping:
    - A bed belongs to one ICU unit.
    - Devices can be mapped to this bed.
    - Patients can later be admitted to this bed.
    """

    id: Optional[int]
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