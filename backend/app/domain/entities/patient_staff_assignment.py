from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PatientStaffAssignment:
    """
    Domain entity representing active or historical staff assignment
    for a patient.

    Supports patient details, care team display, shift handover,
    and future assignment history.
    """

    patient_id: int
    user_id: int
    assignment_type: str

    id: Optional[int] = None
    assigned_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    is_active: bool = True

    # Read-side enrichment fields populated when joined with user data.
    staff_name: Optional[str] = None
    staff_role: Optional[str] = None