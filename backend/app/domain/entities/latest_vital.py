# app/domain/entities/latest_vital.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LatestVital:
    """
    Domain entity representing the latest
    live vital snapshot of a patient.

    This entity is optimized for:
    - ICU dashboard rendering
    - Real-time monitoring
    - Bed-wise patient cards
    """

    id: Optional[int] = None

    patient_id: Optional[int] = None
    bed_id: Optional[int] = None
    device_id: Optional[int] = None

    hr: Optional[float] = None
    bp_sys: Optional[float] = None
    bp_dia: Optional[float] = None
    spo2: Optional[float] = None
    temp: Optional[float] = None
    rr: Optional[float] = None

    status: Optional[str] = None

    recorded_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None