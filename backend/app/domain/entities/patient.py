# app/domain/entities/patient.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from app.domain.enums.patient import Gender


@dataclass
class Patient:
    """
    Domain entity representing an admitted ICU patient.

    Current phase:
    --------------
    This entity contains both patient master details and active
    admission details.

    Future phase:
    -------------
    Patient master and patient encounter/admission will be split
    into separate entities.
    """

    id: Optional[int] = None

    # Patient identifiers
    mrn: Optional[str] = None
    cr_number: Optional[str] = None

    # Patient demographics
    name: str = ""
    contact_number: Optional[str] = None
    age: Optional[int] = None
    gender: Gender = Gender.MALE
    blood_group: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None

    # Admission / ICU context
    bed: Any = None
    bed_id: Optional[int] = None
    diagnosis: Optional[str] = None
    doctor: Optional[str] = None
    admission_time: Optional[datetime] = None
    hospital_id: Optional[int] = None
    status: str = "admitted"

    # Clinical history
    history: list[str] = field(default_factory=list)
    comorbidities: list[str] = field(default_factory=list)

    # Related clinical data
    vitals: list[Any] = field(default_factory=list)
    timeline: list[Any] = field(default_factory=list)