from typing import Optional

from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.providers.lab_result import LabResultProvider
from app.api.schemas.lab_result import LabResultCreateRequest, LabResultResponse
from app.application.lab_results.use_cases.create_lab_result import CreateLabResultUseCase
from app.application.lab_results.use_cases.get_latest_lab_result import GetLatestLabResultUseCase
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(prefix="/patients", tags=["Lab Results"])


def patient_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(PermissionModule.PATIENTS, action)
    )


@router.post(
    "/{patient_id}/lab-results",
    response_model=LabResultResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_lab_result(
    patient_id: int,
    payload: LabResultCreateRequest,
    current_user=patient_permission(PermissionAction.CREATE),
    use_case: CreateLabResultUseCase = Depends(
        LabResultProvider.get_create_use_case
    ),
) -> LabResultResponse:
    """
    Record a lab result for a patient.
    """
    result = use_case.execute(
        patient_id=patient_id,
        ph=payload.ph,
        pao2=payload.pao2,
        paco2=payload.paco2,
        hco3=payload.hco3,
        rbs=payload.rbs,
    )
    return LabResultResponse.model_validate(result)


@router.get(
    "/{patient_id}/lab-results/latest",
    response_model=Optional[LabResultResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_latest_lab_result(
    patient_id: int,
    current_user=patient_permission(PermissionAction.VIEW),
    use_case: GetLatestLabResultUseCase = Depends(
        LabResultProvider.get_latest_use_case
    ),
) -> Optional[LabResultResponse]:
    """
    Return the most recent lab result for a patient.
    """
    result = use_case.execute(patient_id=patient_id)
    if result is None:
        return None
    return LabResultResponse.model_validate(result)
