from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.alarm_repository import AlarmRepository
from app.domain.repositories.clinical_note_repository import (
    ClinicalNoteRepository,
)
from app.domain.repositories.device_master_repository import DeviceMasterRepository
from app.domain.repositories.latest_vital_repository import LatestVitalRepository
from app.domain.repositories.patient_repository import PatientRepository
from app.domain.repositories.patient_staff_assignment_repository import (
    PatientStaffAssignmentRepository,
)
from app.domain.repositories.vital_repository import VitalRepository


class GetPatientDetailsUseCase:
    """
    Aggregates all patient details data required by the Patient Details page.

    Sections:
    - Overview
    - Latest Vitals
    - Vitals / Flowsheet
    - Devices
    - Alarms
    - Timeline
    - Staff Assignment
    - Clinical Notes
    - Reports placeholder
    """

    def __init__(
        self,
        patient_repository: PatientRepository,
        latest_vital_repository: LatestVitalRepository,
        vital_repository: VitalRepository,
        device_repository: DeviceMasterRepository,
        alarm_repository: AlarmRepository,
        patient_staff_assignment_repository: PatientStaffAssignmentRepository,
        clinical_note_repository: ClinicalNoteRepository,
    ):
        self.patient_repository = patient_repository
        self.latest_vital_repository = latest_vital_repository
        self.vital_repository = vital_repository
        self.device_repository = device_repository
        self.alarm_repository = alarm_repository
        self.patient_staff_assignment_repository = (
            patient_staff_assignment_repository
        )
        self.clinical_note_repository = clinical_note_repository

    def execute(self, patient_id: int) -> dict:
        """
        Build patient details response.
        """
        patient = self.patient_repository.by_id(patient_id)

        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        latest_vitals = self.latest_vital_repository.get_by_patient_id(
            patient_id
        )
        vitals = self.vital_repository.list_by_patient_id(patient_id)
        alarms = self.alarm_repository.by_patient(patient_id)
        notes = self.clinical_note_repository.list_by_patient_id(patient_id)

        devices = []
        if patient.bed_id:
            devices = self.device_repository.list_by_bed_id(patient.bed_id)

        staff_assignments = (
            self.patient_staff_assignment_repository.list_active_by_patient_id(
                patient_id
            )
        )

        active_alarm_count = len(
            [
                alarm
                for alarm in alarms
                if not alarm.acknowledged
            ]
        )

        return {
            "overview": {
                "patient": patient,
                "latest_vitals": latest_vitals,
                "active_alarm_count": active_alarm_count,
                "device_count": len(devices),
                "unit_id": getattr(
                    getattr(patient, "bed", None),
                    "icu_unit_id",
                    None,
                ),
            },
            "staff_assignment": staff_assignments,
            "vitals": vitals,
            "devices": devices,
            "alarms": alarms,
            "timeline": patient.timeline,
            "notes": notes,
            "reports": [],
        }