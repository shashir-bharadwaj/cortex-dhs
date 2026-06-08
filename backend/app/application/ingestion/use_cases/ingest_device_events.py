from datetime import datetime, timezone
from typing import Any

from app.core.websocket_manager import websocket_manager
from app.domain.entities.latest_vital import LatestVital
from app.domain.enums.websocket_event import WebSocketEventType


class IngestDeviceEventsUseCase:
    """
    Use case for ingesting canonical device events from the Edge SDK.

    Responsibilities:
    -----------------
    - Resolve external bed code to Cortex BedMaster.
    - Resolve active patient assigned to that bed.
    - Convert measurement events into historical Vital rows.
    - Upsert latest patient vital snapshot.
    - Broadcast live vital updates over WebSocket.
    - Convert alarm events into Alarm rows.
    - Broadcast live alarm updates over WebSocket.
    - Return ingestion summary.
    """

    METRIC_MAPPING = {
        "heart_rate": "hr",
        "hr": "hr",
        "spo2": "spo2",
        "oxygen_saturation": "spo2",
        "temperature": "temp",
        "temp": "temp",
        "respiratory_rate": "rr",
        "rr": "rr",
        "bp_systolic": "bp_sys",
        "systolic_bp": "bp_sys",
        "bp_diastolic": "bp_dia",
        "diastolic_bp": "bp_dia",
    }

    SEVERITY_MAPPING = {
        "critical": "Critical",
        "high": "Critical",
        "severe": "Critical",
        "fatal": "Critical",
        "warning": "Warning",
        "warn": "Warning",
        "medium": "Warning",
        "moderate": "Warning",
        "info": "Info",
        "informational": "Info",
        "low": "Info",
        "normal": "Info",
    }

    def __init__(
        self,
        bed_repository,
        patient_repository,
        vital_repository,
        latest_vital_repository,
        alarm_repository,
    ):
        self.bed_repository = bed_repository
        self.patient_repository = patient_repository
        self.vital_repository = vital_repository
        self.latest_vital_repository = latest_vital_repository
        self.alarm_repository = alarm_repository

    async def execute(
        self,
        events: list[Any],
    ) -> dict:
        """
        Process a batch of device events from the Edge SDK.

        This method is async because measurement and alarm events
        broadcast live updates over WebSocket after persistence.
        """
        received = len(events)
        processed = 0
        vitals_created = 0
        alarms_created = 0
        failed = 0

        for event in events:
            try:
                bed = self._resolve_bed(event)

                if not bed:
                    failed += 1
                    continue

                patient = self._resolve_patient(bed)

                if not patient:
                    failed += 1
                    continue

                event_type = event.event_type.lower()

                if event_type == "measurement":
                    created = await self._create_vital(
                        event=event,
                        patient=patient,
                        bed=bed
                    )

                    if created:
                        processed += 1
                        vitals_created += 1
                    else:
                        failed += 1

                elif event_type == "alarm":
                    await self._create_alarm(
                        event=event,
                        patient=patient,
                        bed=bed,
                    )

                    processed += 1
                    alarms_created += 1

                else:
                    failed += 1

            except Exception:
                failed += 1

        return {
            "received": received,
            "processed": processed,
            "vitals_created": vitals_created,
            "alarms_created": alarms_created,
            "failed": failed,
        }

    def _resolve_bed(
        self,
        event,
    ):
        """
        Resolve external Edge SDK bed code like B1/B2
        to Cortex BedMaster.
        """
        return self.bed_repository.get_by_bed_id(
            event.source.bed_id
        )

    def _resolve_patient(
        self,
        bed,
    ):
        """
        Resolve the currently active patient assigned to the bed.
        """
        return self.patient_repository.get_active_by_bed_id(
            bed.id
        )

    async def _create_vital(
        self,
        event,
        patient,
        bed,
    ) -> bool:
        """
        Create a historical Vital row, update latest live snapshot,
        and broadcast the updated snapshot to subscribed ICU dashboards.
        """
        if not event.metric:
            return False

        if not event.metric.code:
            return False

        metric_field = self.METRIC_MAPPING.get(
            event.metric.code.lower()
        )

        if not metric_field:
            return False

        recorded_at = self._resolve_timestamp(event)

        # Historical vitals table stores one partial row per measurement.
        vital_data = {
            "patient_id": patient.id,
            "hr": None,
            "bp_sys": None,
            "bp_dia": None,
            "spo2": None,
            "temp": None,
            "rr": None,
            "recorded_at": recorded_at,
        }

        vital_data[metric_field] = event.metric.value

        self.vital_repository.create_from_ingestion(
            vital_data
        )

        # Preserve previous snapshot values for metrics that are
        # not present in the current incoming measurement.
        existing_snapshot = (
            self.latest_vital_repository.get_by_patient_id(
                patient.id
            )
        )

        latest_vital = LatestVital(
            patient_id=patient.id,
            bed_id=patient.bed_id,
            device_id=None,
            hr=(
                event.metric.value
                if metric_field == "hr"
                else existing_snapshot.hr
                if existing_snapshot
                else None
            ),
            bp_sys=(
                event.metric.value
                if metric_field == "bp_sys"
                else existing_snapshot.bp_sys
                if existing_snapshot
                else None
            ),
            bp_dia=(
                event.metric.value
                if metric_field == "bp_dia"
                else existing_snapshot.bp_dia
                if existing_snapshot
                else None
            ),
            spo2=(
                event.metric.value
                if metric_field == "spo2"
                else existing_snapshot.spo2
                if existing_snapshot
                else None
            ),
            temp=(
                event.metric.value
                if metric_field == "temp"
                else existing_snapshot.temp
                if existing_snapshot
                else None
            ),
            rr=(
                event.metric.value
                if metric_field == "rr"
                else existing_snapshot.rr
                if existing_snapshot
                else None
            ),
            status="LIVE",
            recorded_at=recorded_at,
        )

        # Upsert latest snapshot before broadcasting so REST reads
        # and WebSocket clients remain consistent.
        self.latest_vital_repository.upsert(
            latest_vital
        )

        await websocket_manager.broadcast_to_unit(
            unit_id=bed.icu_unit_id,
            message={
                "type": WebSocketEventType.LIVE_VITAL_UPDATE,
                "patient_id": patient.id,
                "bed_id": patient.bed_id,
                "unit_id": bed.icu_unit_id,
                "metric": metric_field,
                "value": event.metric.value,
                "recorded_at": recorded_at.isoformat(),
                "snapshot": {
                    "hr": latest_vital.hr,
                    "bp_sys": latest_vital.bp_sys,
                    "bp_dia": latest_vital.bp_dia,
                    "spo2": latest_vital.spo2,
                    "temp": latest_vital.temp,
                    "rr": latest_vital.rr,
                    "status": latest_vital.status,
                },
            },
        )

        return True

    async def _create_alarm(
        self,
        event,
        patient,
        bed,
    ) -> None:
        """
        Create an Alarm row from a canonical alarm event
        and broadcast the live alarm event to subscribed ICU dashboards.
        """
        alarm_data = {
            "timestamp": self._resolve_timestamp(event),
            "patient_id": patient.id,
            "patient_name": patient.name,
            "bed_id": bed.bed_id,
            "device": (
                event.source.device_type
                or event.source.device_id
                or "unknown_device"
            ),
            "message": (
                event.message
                or event.alarm
                or "Device alarm"
            ),
            "severity": self._normalize_alarm_severity(
                event.severity
            ),
            "acknowledged": False,
            "silenced": False,
            "escalated": False,
        }

        created_alarm = (
            self.alarm_repository.create_from_ingestion(
                alarm_data
            )
        )

        await websocket_manager.broadcast_to_unit(
            unit_id=bed.icu_unit_id,
            message={
                "type": WebSocketEventType.LIVE_ALARM_UPDATE,
                "unit_id": bed.icu_unit_id,
                "patient_id": patient.id,
                "patient_name": patient.name,
                "bed_id": bed.bed_id,
                "severity": alarm_data["severity"],
                "message": alarm_data["message"],
                "device": alarm_data["device"],
                "timestamp": alarm_data["timestamp"].isoformat(),
                "alarm_id": (
                    created_alarm.id
                    if created_alarm
                    else None
                ),
            },
        )

    def _normalize_alarm_severity(
        self,
        severity: str | None,
    ) -> str:
        """
        Normalize external Edge SDK/vendor severity
        into Cortex canonical AlarmSeverity values.
        """
        if not severity:
            return "Info"

        normalized = severity.strip().lower()

        return self.SEVERITY_MAPPING.get(
            normalized,
            "Info",
        )

    def _resolve_timestamp(
        self,
        event,
    ) -> datetime:
        """
        Resolve event timestamp using fallback order.
        """
        return (
            event.event_time
            or event.timestamp
            or datetime.now(timezone.utc)
        )