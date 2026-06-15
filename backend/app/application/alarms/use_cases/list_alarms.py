from typing import List

from app.domain.entities.alarm import Alarm
from app.domain.repositories.alarm_repository import AlarmRepository


class ListAlarmsUseCase:
    """
    Use case for listing alarms.
    """

    def __init__(self, alarm_repository: AlarmRepository):
        self.alarm_repository = alarm_repository

    def execute(
        self,
        hospital_id: str | None = None,
        unit_id: str | None = None,
        severity: str | None = None,
        acknowledged: bool | None = None,
        silenced: bool | None = None,
        patient_id: int | None = None,
    ) -> List[Alarm]:
        return self.alarm_repository.list(
            hospital_id=hospital_id,
            unit_id=unit_id,
            severity=severity,
            acknowledged=acknowledged,
            silenced=silenced,
            patient_id=patient_id,
        )