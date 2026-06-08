from typing import List

from app.domain.entities.alarm import Alarm
from app.domain.repositories.alarm_repository import AlarmRepository


class GetPatientAlarmsUseCase:
    """
    Use case for listing alarms for a patient.
    """

    def __init__(self, alarm_repository: AlarmRepository):
        self.alarm_repository = alarm_repository

    def execute(self, patient_id: int) -> List[Alarm]:
        return self.alarm_repository.list_by_patient(patient_id)