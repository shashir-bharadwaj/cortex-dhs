# app/domain/entities/vital.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Vital:
    """
    Domain entity representing a patient's vital record.

    This follows the business/API-facing vital shape,
    while repositories/mappers handle DB translation separately.
    """

    id: Optional[int] = None
    patient_id: Optional[int] = None

    hr: Optional[float] = None
    bp_sys: Optional[float] = None
    bp_dia: Optional[float] = None
    spo2: Optional[float] = None
    temp: Optional[float] = None
    rr: Optional[float] = None

    recorded_at: Optional[datetime] = None