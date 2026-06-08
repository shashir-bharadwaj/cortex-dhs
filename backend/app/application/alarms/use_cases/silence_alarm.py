from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.alarm import Alarm
from app.domain.repositories.alarm_repository import AlarmRepository


class SilenceAlarmUseCase:
    """
    Use case for silencing an alarm.
    """

    def __init__(self, alarm_repository: AlarmRepository):
        self.alarm_repository = alarm_repository

    def execute(self, alarm_id: int) -> Alarm:
        alarm = self.alarm_repository.by_id(alarm_id)

        if not alarm:
            raise ResourceNotFoundError(
                message="Alarm not found.",
                meta={"alarm_id": alarm_id},
            )

        return self.alarm_repository.silence(alarm_id)