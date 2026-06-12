from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LabResult:
    """
    Domain entity representing arterial blood gas and lab values for an ICU patient.
    """

    id: Optional[int] = None
    patient_id: Optional[int] = None

    ph: Optional[float] = None
    pao2: Optional[float] = None
    paco2: Optional[float] = None
    hco3: Optional[float] = None
    rbs: Optional[float] = None

    recorded_at: Optional[datetime] = None
