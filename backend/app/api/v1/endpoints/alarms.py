from fastapi import APIRouter, Depends, Query, status

from app.api.providers.alarms import AlarmProvider
from app.api.providers.auth import AuthProvider
from app.api.schemas.alarm import (
    AcknowledgeAlarmRequest,
    AlarmCreateRequest,
    AlarmResponse,
    EscalateAlarmRequest,
    SilenceAlarmRequest,
)
from app.application.alarms.use_cases.acknowledge_alarm import (
    AcknowledgeAlarmUseCase,
)
from app.application.alarms.use_cases.create_alarm import CreateAlarmUseCase
from app.application.alarms.use_cases.escalate_alarm import EscalateAlarmUseCase
from app.application.alarms.use_cases.list_alarms import ListAlarmsUseCase
from app.application.alarms.use_cases.silence_alarm import SilenceAlarmUseCase
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.alarm import AlarmSeverity
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(
    prefix="/alarms",
    tags=["Alarms"],
)


def alarm_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for Alarm routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.ALARMS,
            action,
        )
    )


@router.get(
    "",
    response_model=list[AlarmResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_alarms(
    hospital_id: str | None = Query(None, alias="hospitalId"),
    unit_id: str | None = Query(None, alias="unitId"),
    severity: AlarmSeverity | None = None,
    acknowledged: bool | None = None,
    silenced: bool | None = None,
    patient_id: int | None = Query(None, alias="patientId"),
    _current_user=alarm_permission(PermissionAction.VIEW),
    use_case: ListAlarmsUseCase = Depends(
        AlarmProvider.list_alarms_use_case
    ),
) -> list[AlarmResponse]:
    """
    List alarms with optional filtering.
    """
    alarms = use_case.execute(
        hospital_id=hospital_id,
        unit_id=unit_id,
        severity=severity.value if severity else None,
        acknowledged=acknowledged,
        silenced=silenced,
        patient_id=patient_id,
    )

    return [
        AlarmResponse.model_validate(alarm)
        for alarm in alarms
    ]


@router.post(
    "",
    response_model=AlarmResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_alarm(
    payload: AlarmCreateRequest,
    _current_user=alarm_permission(PermissionAction.CREATE),
    use_case: CreateAlarmUseCase = Depends(
        AlarmProvider.create_alarm_use_case
    ),
) -> AlarmResponse:
    """
    Create a new alarm.
    """
    alarm = use_case.execute(
        patient_id=payload.patient_id,
        patient_name=payload.patient_name,
        bed_id=payload.bed_id,
        device=payload.device,
        message=payload.message,
        severity=payload.severity,
    )

    return AlarmResponse.model_validate(alarm)


@router.patch(
    "/{alarm_id}/acknowledge",
    response_model=AlarmResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def acknowledge_alarm(
    alarm_id: int,
    payload: AcknowledgeAlarmRequest,
    _current_user=alarm_permission(PermissionAction.MODIFY),
    use_case: AcknowledgeAlarmUseCase = Depends(
        AlarmProvider.acknowledge_alarm_use_case
    ),
) -> AlarmResponse:
    """
    Acknowledge an active alarm.
    """
    alarm = use_case.execute(
        alarm_id=alarm_id,
        acknowledged_by=payload.acknowledged_by,
    )

    return AlarmResponse.model_validate(alarm)


@router.patch(
    "/{alarm_id}/silence",
    response_model=AlarmResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def silence_alarm(
    alarm_id: int,
    payload: SilenceAlarmRequest,
    _current_user=alarm_permission(PermissionAction.MODIFY),
    use_case: SilenceAlarmUseCase = Depends(
        AlarmProvider.silence_alarm_use_case
    ),
) -> AlarmResponse:
    """
    Silence an alarm for a configured duration.
    """
    alarm = use_case.execute(
        alarm_id=alarm_id,
        silenced_by=payload.silenced_by,
        duration_minutes=payload.duration_minutes,
    )

    return AlarmResponse.model_validate(alarm)


@router.patch(
    "/{alarm_id}/escalate",
    response_model=AlarmResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def escalate_alarm(
    alarm_id: int,
    payload: EscalateAlarmRequest,
    _current_user=alarm_permission(PermissionAction.MODIFY),
    use_case: EscalateAlarmUseCase = Depends(
        AlarmProvider.escalate_alarm_use_case
    ),
) -> AlarmResponse:
    """
    Escalate an alarm to another role/user/group.
    """
    alarm = use_case.execute(
        alarm_id=alarm_id,
        escalated_by=payload.escalated_by,
        escalate_to=payload.escalate_to,
    )

    return AlarmResponse.model_validate(alarm)