from app.domain.entities.alarm import Alarm
from app.domain.repositories.alarm_repository import AlarmRepository


class CreateAlarmUseCase:
    """
    Use case for creating an alarm.
    """

    def __init__(self, alarm_repository: AlarmRepository):
        self.alarm_repository = alarm_repository

    def execute(self, alarm: Alarm) -> Alarm:
        return self.alarm_repository.create(alarm)