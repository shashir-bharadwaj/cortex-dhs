from typing import Optional

from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.providers.ventilator_setting import VentilatorSettingProvider
from app.api.schemas.ventilator_setting import (
    VentilatorSettingCreateRequest,
    VentilatorSettingResponse,
)
from app.application.ventilator.use_cases.create_ventilator_setting import (
    CreateVentilatorSettingUseCase,
)
from app.application.ventilator.use_cases.get_latest_ventilator_setting import (
    GetLatestVentilatorSettingUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(prefix="/patients", tags=["Ventilator Settings"])


def patient_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(PermissionModule.PATIENTS, action)
    )


@router.post(
    "/{patient_id}/ventilator-settings",
    response_model=VentilatorSettingResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_ventilator_setting(
    patient_id: int,
    payload: VentilatorSettingCreateRequest,
    current_user=patient_permission(PermissionAction.CREATE),
    use_case: CreateVentilatorSettingUseCase = Depends(
        VentilatorSettingProvider.get_create_use_case
    ),
) -> VentilatorSettingResponse:
    """
    Record ventilator parameters for a patient.
    """
    setting = use_case.execute(
        patient_id=patient_id,
        mode=payload.mode,
        fio2=payload.fio2,
        peep=payload.peep,
        set_rr=payload.set_rr,
        tidal_volume=payload.tidal_volume,
    )
    return VentilatorSettingResponse.model_validate(setting)


@router.get(
    "/{patient_id}/ventilator-settings/latest",
    response_model=Optional[VentilatorSettingResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_latest_ventilator_setting(
    patient_id: int,
    current_user=patient_permission(PermissionAction.VIEW),
    use_case: GetLatestVentilatorSettingUseCase = Depends(
        VentilatorSettingProvider.get_latest_use_case
    ),
) -> Optional[VentilatorSettingResponse]:
    """
    Return the most recent ventilator setting for a patient.
    """
    setting = use_case.execute(patient_id=patient_id)
    if setting is None:
        return None
    return VentilatorSettingResponse.model_validate(setting)
