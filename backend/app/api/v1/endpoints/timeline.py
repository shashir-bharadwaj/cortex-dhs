from typing import List

from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.providers.timeline import TimelineProvider
from app.api.schemas.timeline import (
    TimelineEventModelCreateRequest,
    TimelineEventModelResponse,
)
from app.application.timeline.use_cases.create_timeline_event import (
    CreateTimelineEventUseCase,
)
from app.application.timeline.use_cases.list_patient_timeline import (
    ListPatientTimelineUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)

router = APIRouter(
    prefix="/patients/{patient_id}/timeline",
    tags=["Timeline"],
)


def timeline_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for Timeline routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.TIMELINE,
            action,
        )
    )


# =========================================================
# Response Mappers
# =========================================================

def to_timeline_response(
    timeline_event,
) -> TimelineEventModelResponse:
    """
    Convert timeline event entity into API response schema.
    """
    return TimelineEventModelResponse.model_validate(
        timeline_event
    )


# =========================================================
# Timeline Routes
# =========================================================

@router.post(
    "",
    response_model=TimelineEventModelResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_timeline_event(
    patient_id: int,
    payload: TimelineEventModelCreateRequest,
    _current_user=timeline_permission(
        PermissionAction.CREATE
    ),
    use_case: CreateTimelineEventUseCase = Depends(
        TimelineProvider.get_create_timeline_event_use_case
    ),
) -> TimelineEventModelResponse:
    """
    Create a new timeline event for a patient.
    """
    timeline_event = use_case.execute(
        patient_id=patient_id,
        event=payload.event,
        type=payload.type,
    )

    return to_timeline_response(timeline_event)


@router.get(
    "",
    response_model=List[TimelineEventModelResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_patient_timeline(
    patient_id: int,
    _current_user=timeline_permission(
        PermissionAction.VIEW
    ),
    use_case: ListPatientTimelineUseCase = Depends(
        TimelineProvider.get_list_patient_timeline_use_case
    ),
) -> List[TimelineEventModelResponse]:
    """
    Return patient timeline events ordered newest first.
    """
    timeline_events = use_case.execute(
        patient_id=patient_id
    )

    return [
        to_timeline_response(event)
        for event in timeline_events
    ]