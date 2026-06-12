from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FluidBalance:
    """
    Domain entity representing a fluid intake/output record for an ICU patient.
    """

    id: Optional[int] = None
    patient_id: Optional[int] = None

    in_ml: Optional[float] = None
    out_ml: Optional[float] = None
    source: Optional[str] = None

    recorded_at: Optional[datetime] = None
