# app/domain/entities/patient.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from app.domain.enums.patient import Gender


@dataclass
class Patient:
    """
    Domain entity representing an ICU patient.
    """

    id: Optional[int] = None

    name: str = ""
    age: Optional[int] = None

    gender: Gender = Gender.MALE

    bed_id: Optional[int] = None

    diagnosis: Optional[str] = None

    weight: Optional[float] = None
    height: Optional[float] = None

    blood_group: Optional[str] = None
    doctor: Optional[str] = None

    admission_time: Optional[datetime] = None

    hospital_id: Optional[int] = None

    status: str = "admitted"

    history: list[str] = field(default_factory=list)
    comorbidities: list[str] = field(default_factory=list)

    vitals: list[Any] = field(default_factory=list)
    timeline: list[Any] = field(default_factory=list)