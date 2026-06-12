from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.enums.medication import MedicationOrderType, MedicationStatus


@dataclass
class MedicationOrder:
    """
    Domain entity representing a medication order for an ICU patient.
    Infusion orders include rate, remaining volume, and estimated end time.
    """

    id: Optional[int] = None
    patient_id: Optional[int] = None

    drug_name: str = ""
    order_type: MedicationOrderType = MedicationOrderType.PRN
    dose: Optional[str] = None
    route: Optional[str] = None
    schedule: Optional[str] = None
    status: MedicationStatus = MedicationStatus.PENDING

    # Infusion-specific fields
    rate_ml_hr: Optional[float] = None
    remaining_vol_ml: Optional[float] = None
    est_end_time: Optional[datetime] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
