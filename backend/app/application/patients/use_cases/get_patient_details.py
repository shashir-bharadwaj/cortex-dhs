from datetime import datetime, timezone

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.alarm_repository import AlarmRepository
from app.domain.repositories.clinical_note_repository import ClinicalNoteRepository
from app.domain.repositories.device_master_repository import DeviceMasterRepository
from app.domain.repositories.fluid_balance_repository import FluidBalanceRepository
from app.domain.repositories.lab_result_repository import LabResultRepository
from app.domain.repositories.latest_vital_repository import LatestVitalRepository
from app.domain.repositories.medication_order_repository import MedicationOrderRepository
from app.domain.repositories.patient_repository import PatientRepository
from app.domain.repositories.patient_staff_assignment_repository import (
    PatientStaffAssignmentRepository,
)
from app.domain.repositories.ventilator_setting_repository import VentilatorSettingRepository
from app.domain.repositories.vital_repository import VitalRepository


class GetPatientDetailsUseCase:
    """
    Aggregates all patient details data required by the Patient Details page.

    Sections:
    - Overview (patient, latest vitals, alarm count, device count, unit)
    - Staff Assignment
    - Vitals / Flowsheet
    - Devices
    - Alarms
    - Timeline
    - Clinical Notes
    - Ventilator Parameters
    - Lab Data
    - Fluid Balance (daily I/O)
    - Medication Orders
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
        ventilator_repository: VentilatorSettingRepository,
        lab_result_repository: LabResultRepository,
        fluid_balance_repository: FluidBalanceRepository,
        medication_order_repository: MedicationOrderRepository,
    ):
        self.patient_repository = patient_repository
        self.latest_vital_repository = latest_vital_repository
        self.vital_repository = vital_repository
        self.device_repository = device_repository
        self.alarm_repository = alarm_repository
        self.patient_staff_assignment_repository = patient_staff_assignment_repository
        self.clinical_note_repository = clinical_note_repository
        self.ventilator_repository = ventilator_repository
        self.lab_result_repository = lab_result_repository
        self.fluid_balance_repository = fluid_balance_repository
        self.medication_order_repository = medication_order_repository

    def execute(self, patient_id: int) -> dict:
        patient = self.patient_repository.by_id(patient_id)

        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        latest_vitals = self.latest_vital_repository.get_by_patient_id(patient_id)
        vitals = self.vital_repository.list_by_patient_id(patient_id)
        alarms = self.alarm_repository.by_patient(patient_id)
        notes = self.clinical_note_repository.list_by_patient_id(patient_id)

        devices = []
        if patient.bed_id:
            devices = self.device_repository.list_by_bed_id(patient.bed_id)

        staff_assignments = (
            self.patient_staff_assignment_repository.list_active_by_patient_id(patient_id)
        )

        # New clinical modules
        ventilator_params = self.ventilator_repository.get_latest_by_patient_id(patient_id)
        lab_data = self.lab_result_repository.get_latest_by_patient_id(patient_id)
        medications = self.medication_order_repository.list_by_patient_id(patient_id)

        today = datetime.now(timezone.utc).date()
        daily_fluid_records = self.fluid_balance_repository.list_by_patient_id_and_date(
            patient_id, today
        )
        total_in = sum(r.in_ml or 0.0 for r in daily_fluid_records)
        total_out = sum(r.out_ml or 0.0 for r in daily_fluid_records)
        fluid_balance = {
            "patient_id": patient_id,
            "date": today.isoformat(),
            "in_ml": total_in,
            "out_ml": total_out,
            "balance_ml": total_in - total_out,
        }

        active_alarm_count = len([a for a in alarms if not a.acknowledged])

        return {
            "overview": {
                "patient": patient,
                "latest_vitals": latest_vitals,
                "active_alarm_count": active_alarm_count,
                "device_count": len(devices),
                "unit_id": getattr(getattr(patient, "bed", None), "icu_unit_id", None),
            },
            "staff_assignment": staff_assignments,
            "vitals": vitals,
            "devices": devices,
            "alarms": alarms,
            "timeline": patient.timeline,
            "notes": notes,
            "ventilator_params": ventilator_params,
            "lab_data": lab_data,
            "fluid_balance": fluid_balance,
            "medications": medications,
            "reports": [],
        }
