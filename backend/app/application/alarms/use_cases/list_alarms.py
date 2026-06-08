from typing import List

from app.domain.entities.alarm import Alarm
from app.domain.repositories.alarm_repository import AlarmRepository


class ListAlarmsUseCase:
    """
    Use case for listing alarms.
    """

    def __init__(self, alarm_repository: AlarmRepository):
        self.alarm_repository = alarm_repository

    def execute(self) -> List[Alarm]:
        return self.alarm_repository.list()