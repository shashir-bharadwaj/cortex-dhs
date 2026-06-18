from datetime import datetime, timezone
from typing import List

from app.api.schemas.handover import (
    HandoverNote,
    HandoverPatientCard,
    HandoverVitals,
    ShiftHandoverResponse,
    ShiftInfo,
)
from app.domain.repositories.alarm_repository import AlarmRepository
from app.domain.repositories.clinical_note_repository import ClinicalNoteRepository
from app.domain.repositories.latest_vital_repository import LatestVitalRepository
from app.domain.repositories.nurse_task_repository import NurseTaskRepository
from app.domain.repositories.patient_repository import PatientRepository
from app.domain.repositories.ventilator_setting_repository import VentilatorSettingRepository


def _current_shift() -> ShiftInfo:
    hour = datetime.now(timezone.utc).hour
    if 7 <= hour < 15:
        return ShiftInfo(name="Morning", start="07:00", end="15:00")
    elif 15 <= hour < 23:
        return ShiftInfo(name="Evening", start="15:00", end="23:00")
    else:
        return ShiftInfo(name="Night", start="23:00", end="07:00")


class GetShiftSummaryUseCase:

    def __init__(
        self,
        patient_repository: PatientRepository,
        latest_vital_repository: LatestVitalRepository,
        alarm_repository: AlarmRepository,
        nurse_task_repository: NurseTaskRepository,
        clinical_note_repository: ClinicalNoteRepository,
        ventilator_setting_repository: VentilatorSettingRepository,
    ):
        self.patient_repository = patient_repository
        self.latest_vital_repository = latest_vital_repository
        self.alarm_repository = alarm_repository
        self.nurse_task_repository = nurse_task_repository
        self.clinical_note_repository = clinical_note_repository
        self.ventilator_setting_repository = ventilator_setting_repository

    def execute(self) -> ShiftHandoverResponse:
        patients = self.patient_repository.list_all()
        if not patients:
            return ShiftHandoverResponse(shift=_current_shift(), patients=[])

        patient_ids = [p.id for p in patients]

        # Batch fetch vitals and alarms
        vitals_map = self.latest_vital_repository.list_by_patient_ids(patient_ids)
        active_alarms = self.alarm_repository.list_active_by_patient_ids(patient_ids)
        alarm_counts: dict[int, int] = {}
        for alarm in active_alarms:
            if not alarm.acknowledged:
                alarm_counts[alarm.patient_id] = alarm_counts.get(alarm.patient_id, 0) + 1

        cards: List[HandoverPatientCard] = []
        for patient in patients:
            vital = vitals_map.get(patient.id)
            bp = None
            if vital and vital.bp_sys and vital.bp_dia:
                bp = f"{int(vital.bp_sys)}/{int(vital.bp_dia)}"

            vitals = HandoverVitals(
                hr=vital.hr if vital else None,
                spo2=vital.spo2 if vital else None,
                bp=bp,
                rr=vital.rr if vital else None,
                temp=vital.temp if vital else None,
            )

            # Latest clinical note
            notes = self.clinical_note_repository.list_by_patient_id(patient.id)
            latest_note = None
            if notes:
                n = notes[0]
                latest_note = HandoverNote(text=n.note_text, author=n.author_name)

            # Ventilator active
            vent = self.ventilator_setting_repository.get_latest_by_patient_id(patient.id)

            # Pending tasks
            pending_tasks = self.nurse_task_repository.count_pending_by_patient(patient.id)

            bed_label = ""
            if patient.bed:
                bed_label = patient.bed.bed_id
            elif patient.bed_id:
                bed_label = str(patient.bed_id)

            cards.append(
                HandoverPatientCard(
                    patient_id=patient.id,
                    bed_label=bed_label,
                    patient_name=patient.name,
                    age=patient.age,
                    gender=patient.gender.value if patient.gender else None,
                    diagnosis=patient.diagnosis,
                    vitals=vitals,
                    doctor=patient.doctor,
                    unacknowledged_alarms=alarm_counts.get(patient.id, 0),
                    pending_tasks=pending_tasks,
                    latest_note=latest_note,
                    ventilator_active=vent is not None,
                )
            )

        return ShiftHandoverResponse(shift=_current_shift(), patients=cards)
