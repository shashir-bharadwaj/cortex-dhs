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

    history: List[str] = Field(default_factory=list)
    comorbidities: List[str] = Field(default_factory=list)

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

    history: List[str] = Field(default_factory=list)
    comorbidities: List[str] = Field(default_factory=list)

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


class LatestVitalResponse(BaseModel):
    """
    Response schema for the latest live vital snapshot.
    """

    id: Optional[int] = None

    patient_id: Optional[int] = Field(default=None, alias="patientId")
    bed_id: Optional[int] = Field(default=None, alias="bedId")
    device_id: Optional[int] = Field(default=None, alias="deviceId")

    hr: Optional[float] = None
    bp_sys: Optional[float] = Field(default=None, alias="bpSys")
    bp_dia: Optional[float] = Field(default=None, alias="bpDia")
    spo2: Optional[float] = None
    temp: Optional[float] = None
    rr: Optional[float] = None

    status: Optional[str] = None

    recorded_at: Optional[datetime] = Field(default=None, alias="recordedAt")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

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

    history: List[str] = Field(default_factory=list)
    comorbidities: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PatientDetailResponse(PatientResponse):
    """
    Detailed patient response including ICU-related relationships.
    """

    vitals: List[VitalResponse] = Field(default_factory=list)
    timeline: List[TimelineEventModelResponse] = Field(default_factory=list)


class PatientOverviewResponse(BaseModel):
    """
    Tab-ready response for the patient overview section.
    """

    patient: PatientResponse
    latest_vitals: Optional[LatestVitalResponse] = Field(
        default=None,
        alias="latestVitals",
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)