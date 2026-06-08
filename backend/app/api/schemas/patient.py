# app/api/schemas/patient.py

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.vitals import VitalResponse
from app.domain.enums.patient import Gender


class PatientCreateRequest(BaseModel):
    """
    Request schema for creating a patient.
    """

    name: str
    age: Optional[int] = None
    gender: Gender = Gender.MALE

    bed_id: Optional[int] = Field(default=None, alias="bedId")
    diagnosis: Optional[str] = None

    weight: Optional[float] = None
    height: Optional[float] = None

    blood_group: Optional[str] = Field(default=None, alias="bloodGroup")
    doctor: Optional[str] = None

    admission_time: Optional[datetime] = Field(
        default=None,
        alias="admissionTime",
    )

    hospital_id: Optional[int] = Field(default=None, alias="hospitalId")

    history: List[str] = []
    comorbidities: List[str] = []

    model_config = ConfigDict(populate_by_name=True)


class PatientUpdateRequest(BaseModel):
    """
    Request schema for updating a patient.
    """

    name: str
    age: Optional[int] = None
    gender: Gender = Gender.MALE

    bed_id: Optional[int] = Field(default=None, alias="bedId")
    diagnosis: Optional[str] = None

    weight: Optional[float] = None
    height: Optional[float] = None

    blood_group: Optional[str] = Field(default=None, alias="bloodGroup")
    doctor: Optional[str] = None

    admission_time: Optional[datetime] = Field(
        default=None,
        alias="admissionTime",
    )

    hospital_id: Optional[int] = Field(default=None, alias="hospitalId")

    history: List[str] = []
    comorbidities: List[str] = []

    model_config = ConfigDict(populate_by_name=True)


class TimelineEventModelResponse(BaseModel):
    """
    Response schema for patient timeline events.
    """

    id: int
    time: Optional[str] = None
    event: Optional[str] = None
    type: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PatientResponse(BaseModel):
    """
    Basic patient response schema.
    """

    id: int
    name: str
    age: Optional[int] = None
    gender: Gender = Gender.MALE

    bed_id: Optional[int] = Field(default=None, alias="bedId")
    diagnosis: Optional[str] = None

    weight: Optional[float] = None
    height: Optional[float] = None

    blood_group: Optional[str] = Field(default=None, alias="bloodGroup")
    doctor: Optional[str] = None

    admission_time: Optional[datetime] = Field(
        default=None,
        alias="admissionTime",
    )

    hospital_id: Optional[int] = Field(default=None, alias="hospitalId")

    status: str

    history: List[str] = []
    comorbidities: List[str] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PatientDetailResponse(PatientResponse):
    """
    Detailed patient response including ICU-related relationships.
    """

    vitals: List[VitalResponse] = []
    timeline: List[TimelineEventModelResponse] = []