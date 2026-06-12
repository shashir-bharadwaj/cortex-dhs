from collections import defaultdict
from datetime import date, datetime, timezone
from typing import Optional

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.patient_repository import PatientRepository
from app.domain.repositories.vital_repository import VitalRepository


class GetPatientFlowsheetUseCase:
    """
    Build a 24-hour hourly vitals grid for the Flowsheet tab.
    Groups existing vital records by hour and picks the last reading per hour.
    """

    def __init__(
        self,
        patient_repository: PatientRepository,
        vital_repository: VitalRepository,
    ):
        self.patient_repository = patient_repository
        self.vital_repository = vital_repository

    def execute(self, patient_id: int, target_date: Optional[date] = None) -> dict:
        patient = self.patient_repository.by_id(patient_id)
        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        if target_date is None:
            target_date = datetime.now(timezone.utc).date()

        vitals = self.vital_repository.list_by_patient_id(patient_id)

        # Filter to the requested date and group by hour
        hourly: dict[int, dict] = defaultdict(dict)

        for vital in vitals:
            recorded = vital.recorded_at
            if recorded is None:
                continue
            # Normalize to UTC-aware if naive
            if recorded.tzinfo is None:
                recorded = recorded.replace(tzinfo=timezone.utc)
            if recorded.date() != target_date:
                continue
            hour = recorded.hour
            # Keep last-recorded (list is desc by recorded_at so first wins)
            if hour not in hourly:
                hourly[hour] = {
                    "hr": vital.hr,
                    "spo2": vital.spo2,
                    "bp_sys": vital.bp_sys,
                    "bp_dia": vital.bp_dia,
                    "temp": vital.temp,
                    "rr": vital.rr,
                }

        hours_present = sorted(hourly.keys())

        def row(label, extractor):
            return {
                "parameter": label,
                "values": {
                    str(h): extractor(hourly[h]) for h in hours_present
                },
            }

        rows = [
            row("HR (bpm)", lambda v: v.get("hr")),
            row("SpO2 (%)", lambda v: v.get("spo2")),
            row(
                "BP (mmHg)",
                lambda v: (
                    f"{int(v['bp_sys'])}/{int(v['bp_dia'])}"
                    if v.get("bp_sys") and v.get("bp_dia")
                    else None
                ),
            ),
            row("Temp (°F)", lambda v: v.get("temp")),
            row("RR (/min)", lambda v: v.get("rr")),
        ]

        return {
            "patient_id": patient_id,
            "date": target_date.isoformat(),
            "hours": hours_present,
            "rows": rows,
        }
