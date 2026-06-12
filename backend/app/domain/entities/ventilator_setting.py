from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class VentilatorSetting:
    """
    Domain entity representing ventilator parameters for an ICU patient.
    """

    id: Optional[int] = None
    patient_id: Optional[int] = None

    mode: Optional[str] = None
    fio2: Optional[float] = None
    peep: Optional[float] = None
    set_rr: Optional[int] = None
    tidal_volume: Optional[float] = None

    recorded_at: Optional[datetime] = None
