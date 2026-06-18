from typing import List, Optional

from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.providers.nurse_task import NurseTaskProvider
from app.api.schemas.nurse_task import (
    NurseTaskCreateRequest,
    NurseTaskResponse,
    NurseTaskSummaryResponse,
)
from app.application.tasks.use_cases.create_nurse_task import CreateNurseTaskUseCase
from app.application.tasks.use_cases.complete_nurse_task import CompleteNurseTaskUseCase
from app.application.tasks.use_cases.list_nurse_tasks import ListNurseTasksUseCase
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule
from app.domain.enums.task import TaskStatus

router = APIRouter(prefix="/tasks", tags=["Nurse Tasks"])


def task_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(PermissionModule.PATIENTS, action)
    )


@router.get(
    "/",
    response_model=NurseTaskSummaryResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_nurse_tasks(
    task_status: Optional[TaskStatus] = None,
    patient_id: Optional[int] = None,
    current_user=task_permission(PermissionAction.VIEW),
    use_case: ListNurseTasksUseCase = Depends(NurseTaskProvider.get_list_use_case),
) -> NurseTaskSummaryResponse:
    tasks = use_case.execute(status=task_status, patient_id=patient_id)
    task_responses = [NurseTaskResponse.model_validate(t) for t in tasks]

    return NurseTaskSummaryResponse(
        total=len(tasks),
        pending=sum(1 for t in tasks if t.status == TaskStatus.PENDING),
        in_progress=sum(1 for t in tasks if t.status == TaskStatus.IN_PROGRESS),
        completed=sum(1 for t in tasks if t.status == TaskStatus.COMPLETED),
        tasks=task_responses,
    )


@router.post(
    "/",
    response_model=NurseTaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_nurse_task(
    payload: NurseTaskCreateRequest,
    current_user=task_permission(PermissionAction.CREATE),
    use_case: CreateNurseTaskUseCase = Depends(NurseTaskProvider.get_create_use_case),
) -> NurseTaskResponse:
    task = use_case.execute(
        patient_id=payload.patient_id,
        title=payload.title,
        description=payload.description,
        due_time=payload.due_time,
        assigned_to_id=payload.assigned_to_id,
    )
    return NurseTaskResponse.model_validate(task)


@router.patch(
    "/{task_id}/complete",
    response_model=NurseTaskResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def complete_nurse_task(
    task_id: int,
    current_user=task_permission(PermissionAction.MODIFY),
    use_case: CompleteNurseTaskUseCase = Depends(NurseTaskProvider.get_complete_use_case),
) -> NurseTaskResponse:
    task = use_case.execute(task_id=task_id)
    return NurseTaskResponse.model_validate(task)
