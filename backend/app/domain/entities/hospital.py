from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Hospital:
    """
    Domain entity for a hospital.
    """

    id: Optional[int]
    name: str
    code: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    contact_number: Optional[str]
    email: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class HospitalUnit:
    """
    Domain entity for a hospital unit.
    """

    id: Optional[int]
    hospital_id: int
    name: str
    code: Optional[str]
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None