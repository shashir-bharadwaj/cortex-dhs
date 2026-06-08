from dataclasses import dataclass
from typing import Optional


@dataclass
class ICUUnitMaster:
    """
    Domain entity representing an ICU unit managed by admin users.
    """

    id: Optional[int]
    icu_name: str
    type: str
    department: str
    beds: int
    devices: Optional[str]
    gateway: Optional[str]
    status: str