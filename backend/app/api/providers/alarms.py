from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.alarms.use_cases.acknowledge_alarm import (
    AcknowledgeAlarmUseCase,
)
from app.application.alarms.use_cases.create_alarm import CreateAlarmUseCase
from app.application.alarms.use_cases.escalate_alarm import EscalateAlarmUseCase
from app.application.alarms.use_cases.get_patient_alarms import (
    GetPatientAlarmsUseCase,
)
from app.application.alarms.use_cases.list_alarms import ListAlarmsUseCase
from app.application.alarms.use_cases.silence_alarm import SilenceAlarmUseCase
from app.domain.repositories.alarm_repository import AlarmRepository


class AlarmProvider:
    """
    Provider responsible for constructing alarm use cases.

    The provider receives domain repository abstractions from RepositoryProvider
    and wires them into alarm-specific use cases.
    """

    @staticmethod
    def create_alarm_use_case(
        alarm_repository: AlarmRepository = Depends(
            RepositoryProvider.get_alarm_repository
        ),
    ) -> CreateAlarmUseCase:
        return CreateAlarmUseCase(alarm_repository)

    @staticmethod
    def list_alarms_use_case(
        alarm_repository: AlarmRepository = Depends(
            RepositoryProvider.get_alarm_repository
        ),
    ) -> ListAlarmsUseCase:
        return ListAlarmsUseCase(alarm_repository)

    @staticmethod
    def get_patient_alarms_use_case(
        alarm_repository: AlarmRepository = Depends(
            RepositoryProvider.get_alarm_repository
        ),
    ) -> GetPatientAlarmsUseCase:
        return GetPatientAlarmsUseCase(alarm_repository)

    @staticmethod
    def acknowledge_alarm_use_case(
        alarm_repository: AlarmRepository = Depends(
            RepositoryProvider.get_alarm_repository
        ),
    ) -> AcknowledgeAlarmUseCase:
        return AcknowledgeAlarmUseCase(alarm_repository)

    @staticmethod
    def silence_alarm_use_case(
        alarm_repository: AlarmRepository = Depends(
            RepositoryProvider.get_alarm_repository
        ),
    ) -> SilenceAlarmUseCase:
        return SilenceAlarmUseCase(alarm_repository)

    @staticmethod
    def escalate_alarm_use_case(
        alarm_repository: AlarmRepository = Depends(
            RepositoryProvider.get_alarm_repository
        ),
    ) -> EscalateAlarmUseCase:
        return EscalateAlarmUseCase(alarm_repository)