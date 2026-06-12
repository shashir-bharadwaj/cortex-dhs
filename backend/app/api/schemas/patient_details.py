from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.api.schemas.alarm import AlarmResponse
from app.api.schemas.clinical_note import ClinicalNoteResponse
from app.api.schemas.device_master import DeviceMasterResponse
from app.api.schemas.fluid_balance import FluidBalanceSummaryResponse
from app.api.schemas.lab_result import LabResultResponse
from app.api.schemas.latest_vital import LatestVitalResponse
from app.api.schemas.medication_order import MedicationOrderResponse
from app.api.schemas.patient import PatientResponse, TimelineEventModelResponse
from app.api.schemas.ventilator_setting import VentilatorSettingResponse
from app.api.schemas.vitals import VitalResponse


class StaffAssignmentResponse(BaseModel):
    """
    Assigned care team member.
    """

    staff_name: str | None = Field(default=None, alias="staffName")
    staff_role: str | None = Field(default=None, alias="staffRole")
    assignment_type: str = Field(alias="assignmentType")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PatientOverviewResponse(BaseModel):
    """
    Overview section displayed on the patient details page.
    """

    patient: PatientResponse

    latest_vitals: LatestVitalResponse | None = Field(
        default=None,
        alias="latestVitals",
    )

    active_alarm_count: int = Field(default=0, alias="activeAlarmCount")
    device_count: int = Field(default=0, alias="deviceCount")

    unit_id: int | None = Field(default=None, alias="unitId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PatientDetailsResponse(BaseModel):
    """
    Complete patient details response for tab-ready UI rendering.
    """

    overview: PatientOverviewResponse

    staff_assignment: List[StaffAssignmentResponse] = Field(
        default_factory=list,
        alias="staffAssignment",
    )

    vitals: List[VitalResponse] = Field(default_factory=list)
    devices: List[DeviceMasterResponse] = Field(default_factory=list)
    alarms: List[AlarmResponse] = Field(default_factory=list)

    timeline: List[TimelineEventModelResponse] = Field(default_factory=list)
    notes: List[ClinicalNoteResponse] = Field(default_factory=list)

    # New clinical modules
    medications: List[MedicationOrderResponse] = Field(default_factory=list)
    ventilator_params: Optional[VentilatorSettingResponse] = Field(
        default=None, alias="ventilatorParams"
    )
    lab_data: Optional[LabResultResponse] = Field(default=None, alias="labData")
    fluid_balance: Optional[FluidBalanceSummaryResponse] = Field(
        default=None, alias="fluidBalance"
    )

    reports: List[Any] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
