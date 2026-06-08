from datetime import datetime

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.alarm import Alarm
from app.domain.entities.latest_vital import LatestVital
from app.domain.repositories.alarm_repository import AlarmRepository
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.device_master_repository import DeviceMasterRepository
from app.domain.repositories.hospital_repository import HospitalRepository
from app.domain.repositories.latest_vital_repository import (
    LatestVitalRepository,
)
from app.domain.repositories.patient_repository import PatientRepository


class GetDashboardOverviewUseCase:
    """
    Build aggregated ICU dashboard overview response.

    This use case acts as a read-optimized dashboard aggregation layer.
    It intentionally fetches data in batches so the frontend can load the
    landing dashboard with one API call instead of multiple small calls.
    """

    def __init__(
        self,
        hospital_repository: HospitalRepository,
        bed_repository: BedRepository,
        patient_repository: PatientRepository,
        latest_vital_repository: LatestVitalRepository,
        alarm_repository: AlarmRepository,
        device_repository: DeviceMasterRepository,
    ) -> None:
        self.hospital_repository = hospital_repository
        self.bed_repository = bed_repository
        self.patient_repository = patient_repository

        # Latest vitals are read from latest_patient_vitals.
        # This keeps dashboard reads fast and avoids querying
        # historical vitals for every request.
        self.latest_vital_repository = latest_vital_repository

        self.alarm_repository = alarm_repository
        self.device_repository = device_repository

    def execute(self, unit_id: int) -> dict:
        """
        Return complete dashboard overview for a given ICU/unit.

        Aggregates:
        - unit summary
        - bed-wise patient cards
        - latest vitals snapshot
        - monitoring devices
        - alarm indicators
        - recent alarm list
        """

        # ---------------------------------------------------------
        # Fetch ICU unit
        # ---------------------------------------------------------

        unit = self.hospital_repository.get_unit(unit_id)

        if not unit:
            raise ResourceNotFoundError(
                message="Hospital unit not found.",
                meta={"unit_id": unit_id},
            )

        # ---------------------------------------------------------
        # Fetch dashboard source data in batches
        # ---------------------------------------------------------
        # These batch calls avoid N+1 query problems. The dashboard needs
        # many related records at once, so repositories expose grouped
        # read methods instead of calling one query per bed/patient.

        beds = self.bed_repository.list_by_icu_unit_id(unit_id)
        bed_ids = [bed.id for bed in beds]

        patients = self.patient_repository.list_active_by_bed_ids(bed_ids)
        patient_ids = [patient.id for patient in patients]

        # Fetch live patient vitals from the snapshot table.
        # vitals table = historical stream
        # latest_patient_vitals = current dashboard state
        latest_vitals = self.latest_vital_repository.list_by_patient_ids(
            patient_ids
        )

        active_alarms = self.alarm_repository.list_active_by_patient_ids(
            patient_ids
        )

        recent_alarms = self.alarm_repository.list_recent_by_patient_ids(
            patient_ids=patient_ids,
            limit=50,
        )

        monitoring_devices = self.device_repository.list_by_bed_ids(bed_ids)

        # ---------------------------------------------------------
        # Build lookup maps for alarm-related card indicators
        # ---------------------------------------------------------

        alarm_count_map, critical_alarm_map = self._build_alarm_maps(
            active_alarms
        )

        # ---------------------------------------------------------
        # Build bed-wise patient cards and dashboard summary
        # ---------------------------------------------------------

        patient_cards, summary = self._build_patient_cards(
            beds=beds,
            patients=patients,
            latest_vitals=latest_vitals,
            monitoring_devices=monitoring_devices,
            alarm_count_map=alarm_count_map,
            critical_alarm_map=critical_alarm_map,
            active_alarm_count=len(active_alarms),
        )

        # ---------------------------------------------------------
        # Build recent alarm feed
        # ---------------------------------------------------------

        alarms = self._build_alarm_payload(
            alarms=recent_alarms,
            patients=patients,
            beds=beds,
        )

        # ---------------------------------------------------------
        # Final dashboard response
        # ---------------------------------------------------------

        return {
            "unit": {
                "id": unit.id,
                "name": unit.name,
                "department": getattr(unit, "department", None),
                "totalBeds": len(beds),
                "occupiedBeds": len(patients),
            },
            "summary": summary,
            "patientCards": patient_cards,
            "alarms": alarms,
            "generatedAt": datetime.utcnow(),
        }

    def _build_alarm_maps(
        self,
        alarms: list[Alarm],
    ) -> tuple[dict[int, int], dict[int, bool]]:
        """
        Build quick lookup structures for dashboard rendering.

        Why:
        ----
        The dashboard repeatedly needs to know:
        - how many active alarms each patient has
        - whether each patient has any critical alarm

        Precomputing maps keeps patient card generation simple and avoids
        repeatedly scanning the full alarm list for every patient.
        """

        alarm_count_map: dict[int, int] = {}
        critical_alarm_map: dict[int, bool] = {}

        for alarm in alarms:
            alarm_count_map[alarm.patient_id] = (
                alarm_count_map.get(alarm.patient_id, 0) + 1
            )

            if self._severity_value(alarm.severity).upper() == "CRITICAL":
                critical_alarm_map[alarm.patient_id] = True

        return alarm_count_map, critical_alarm_map

    def _build_patient_cards(
        self,
        beds,
        patients,
        latest_vitals: dict[int, LatestVital],
        monitoring_devices: dict[int, list[str]],
        alarm_count_map: dict[int, int],
        critical_alarm_map: dict[int, bool],
        active_alarm_count: int,
    ) -> tuple[list[dict], dict]:
        """
        Build bed-wise patient dashboard cards.

        Each card aggregates:
        - bed metadata
        - patient snapshot
        - latest vitals
        - monitoring devices
        - active alarm count
        - critical alarm indicator
        """

        # Fast lookup for patient currently assigned to each bed.
        patient_by_bed_id = {
            patient.bed_id: patient
            for patient in patients
        }

        patient_cards = []

        normal_count = 0
        warning_count = 0
        critical_count = 0

        for bed in beds:
            patient = patient_by_bed_id.get(bed.id)

            if not patient:
                patient_cards.append(
                    self._build_empty_bed_card(
                        bed=bed,
                        monitoring_devices=monitoring_devices,
                    )
                )
                continue

            status = self._patient_status(
                patient_id=patient.id,
                alarm_count_map=alarm_count_map,
                critical_alarm_map=critical_alarm_map,
            )

            if status == "CRITICAL":
                critical_count += 1
            elif status == "WARNING":
                warning_count += 1
            else:
                normal_count += 1

            patient_cards.append(
                {
                    "bed": {
                        "id": bed.id,
                        "bedId": bed.bed_id,
                    },
                    "patient": {
                        "id": patient.id,
                        "name": patient.name,
                        "age": patient.age,
                        "gender": patient.gender,
                        "diagnosis": patient.diagnosis,
                        # Doctor assignment is intentionally left nullable
                        # until doctor-patient assignment is modeled.
                        "doctor": None,
                    },
                    "status": status,
                    # The vitals object is now resolved from latest_patient_vitals,
                    # so dashboard cards always receive the current live snapshot.
                    "vitals": self._format_vitals(
                        latest_vitals.get(patient.id)
                    ),
                    "monitoring": monitoring_devices.get(bed.id, []),
                    "activeAlarmCount": alarm_count_map.get(patient.id, 0),
                    "hasCriticalAlarm": critical_alarm_map.get(
                        patient.id,
                        False,
                    ),
                }
            )

        summary = {
            "normal": normal_count,
            "warning": warning_count,
            "critical": critical_count,
            "activeAlarms": active_alarm_count,
        }

        return patient_cards, summary

    def _build_empty_bed_card(
        self,
        bed,
        monitoring_devices: dict[int, list[str]],
    ) -> dict:
        """
        Build dashboard card for an unoccupied bed.

        Empty beds are still returned so the frontend can render a complete
        bed grid without making a separate bed-management API call.
        """

        return {
            "bed": {
                "id": bed.id,
                "bedId": bed.bed_id,
            },
            "patient": None,
            "status": "EMPTY",
            "vitals": None,
            "monitoring": monitoring_devices.get(bed.id, []),
            "activeAlarmCount": 0,
            "hasCriticalAlarm": False,
        }

    def _patient_status(
        self,
        patient_id: int,
        alarm_count_map: dict[int, int],
        critical_alarm_map: dict[int, bool],
    ) -> str:
        """
        Determine dashboard status for a patient card.

        Business priority:
        CRITICAL > WARNING > NORMAL
        """

        if critical_alarm_map.get(patient_id):
            return "CRITICAL"

        if alarm_count_map.get(patient_id):
            return "WARNING"

        return "NORMAL"

    def _format_vitals(
        self,
        vitals: LatestVital | None,
    ) -> dict | None:
        """
        Convert latest vitals snapshot into dashboard response format.

        Current behavior:
        - uses latest snapshot only
        - does not return historical vitals
        - does not yet evaluate vital-level thresholds

        Threshold-based vital statuses can later be introduced here.
        """

        if not vitals:
            return None

        return {
            "hr": {
                "value": vitals.hr,
                "unit": "bpm",
                "status": "NORMAL",
                "recordedAt": vitals.recorded_at,
            },
            "spo2": {
                "value": vitals.spo2,
                "unit": "%",
                "status": "NORMAL",
                "recordedAt": vitals.recorded_at,
            },
            "bp": {
                "value": f"{vitals.bp_sys}/{vitals.bp_dia}",
                "unit": "mmHg",
                "status": "NORMAL",
                "recordedAt": vitals.recorded_at,
            },
            "rr": {
                "value": vitals.rr,
                "unit": "/min",
                "status": "NORMAL",
                "recordedAt": vitals.recorded_at,
            },
            "temp": {
                "value": vitals.temp,
                "unit": "F",
                "status": "NORMAL",
                "recordedAt": vitals.recorded_at,
            },
        }

    def _build_alarm_payload(
        self,
        alarms: list[Alarm],
        patients,
        beds,
    ) -> list[dict]:
        """
        Build recent alarm feed shown on the dashboard.

        Each alarm item is enriched with patient and bed context so the
        frontend does not need additional lookups.
        """

        patient_id_to_name = {
            patient.id: patient.name
            for patient in patients
        }

        patient_id_to_bed_id = {
            patient.id: patient.bed_id
            for patient in patients
        }

        bed_id_to_code = {
            bed.id: bed.bed_id
            for bed in beds
        }

        payload = []

        for alarm in alarms:
            payload.append(
                {
                    "id": alarm.id,
                    "patientId": alarm.patient_id,
                    "patientName": patient_id_to_name.get(
                        alarm.patient_id,
                        "Unknown",
                    ),
                    "bedId": bed_id_to_code.get(
                        patient_id_to_bed_id.get(alarm.patient_id),
                        "Unknown",
                    ),
                    # Current Alarm entity stores source/type as device.
                    "alarmType": alarm.device,
                    "deviceSource": alarm.device,
                    "message": alarm.message,
                    "severity": self._severity_value(alarm.severity),
                    "timestamp": alarm.timestamp,
                    "acknowledged": alarm.acknowledged,
                    "silenced": alarm.silenced,
                    "escalated": alarm.escalated,
                }
            )

        return payload

    def _severity_value(self, severity) -> str:
        """
        Normalize enum/string severity values for safe API serialization.
        """

        return severity.value if hasattr(severity, "value") else severity