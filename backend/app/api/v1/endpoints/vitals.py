from typing import List

from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.providers.vitals import VitalProvider
from app.api.schemas.vitals import VitalCreateRequest, VitalResponse
from app.application.vitals.use_cases.create_vital import CreateVitalUseCase
from app.application.vitals.use_cases.get_vital import GetVitalUseCase
from app.application.vitals.use_cases.list_patient_vitals import (
    ListPatientVitalsUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)

router = APIRouter(
    prefix="/patients/{patient_id}/vitals",
    tags=["Vitals"],
)


def vitals_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for Vitals routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.VITALS,
            action,
        )
    )


@router.post(
    "",
    response_model=VitalResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_vital(
    patient_id: int,
    payload: VitalCreateRequest,
    _current_user=vitals_permission(PermissionAction.CREATE),
    use_case: CreateVitalUseCase = Depends(
        VitalProvider.get_create_vital_use_case
    ),
) -> VitalResponse:
    """
    Create a vital record for a patient.
    """
    vital = use_case.execute(
        patient_id=patient_id,
        hr=payload.hr,
        bp_sys=payload.bp_sys,
        bp_dia=payload.bp_dia,
        spo2=payload.spo2,
        temp=payload.temp,
        rr=payload.rr,
        recorded_at=payload.recorded_at,
    )

    return VitalResponse.model_validate(vital)


@router.get(
    "",
    response_model=List[VitalResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_patient_vitals(
    patient_id: int,
    _current_user=vitals_permission(PermissionAction.VIEW),
    use_case: ListPatientVitalsUseCase = Depends(
        VitalProvider.get_list_patient_vitals_use_case
    ),
) -> List[VitalResponse]:
    """
    List all vital records for a patient.
    """
    vitals = use_case.execute(patient_id)

    return [
        VitalResponse.model_validate(vital)
        for vital in vitals
    ]


@router.get(
    "/{vital_id}",
    response_model=VitalResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_vital(
    patient_id: int,
    vital_id: int,
    _current_user=vitals_permission(PermissionAction.VIEW),
    use_case: GetVitalUseCase = Depends(
        VitalProvider.get_get_vital_use_case
    ),
) -> VitalResponse:
    """
    Fetch a specific vital record for a patient.
    """
    vital = use_case.execute(vital_id)

    if vital.patient_id != patient_id:
        raise ResourceNotFoundError(
            message="Vital not found.",
            meta={
                "patient_id": patient_id,
                "vital_id": vital_id,
            },
        )

    return VitalResponse.model_validate(vital)