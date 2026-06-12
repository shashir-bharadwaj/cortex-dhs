from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.api.providers.auth import AuthProvider
from app.api.providers.fluid_balance import FluidBalanceProvider
from app.api.schemas.fluid_balance import (
    FluidBalanceCreateRequest,
    FluidBalanceRecordResponse,
    FluidBalanceSummaryResponse,
)
from app.application.fluid_balance.use_cases.create_fluid_balance_record import (
    CreateFluidBalanceRecordUseCase,
)
from app.application.fluid_balance.use_cases.get_daily_fluid_balance import (
    GetDailyFluidBalanceUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(prefix="/patients", tags=["Fluid Balance"])


def patient_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(PermissionModule.PATIENTS, action)
    )


@router.post(
    "/{patient_id}/fluid-balance",
    response_model=FluidBalanceRecordResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_fluid_balance_record(
    patient_id: int,
    payload: FluidBalanceCreateRequest,
    current_user=patient_permission(PermissionAction.CREATE),
    use_case: CreateFluidBalanceRecordUseCase = Depends(
        FluidBalanceProvider.get_create_use_case
    ),
) -> FluidBalanceRecordResponse:
    """
    Record a fluid intake or output entry for a patient.
    """
    record = use_case.execute(
        patient_id=patient_id,
        in_ml=payload.in_ml,
        out_ml=payload.out_ml,
        source=payload.source,
    )
    return FluidBalanceRecordResponse.model_validate(record)


@router.get(
    "/{patient_id}/fluid-balance/daily",
    response_model=FluidBalanceSummaryResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_daily_fluid_balance(
    patient_id: int,
    target_date: Optional[date] = Query(default=None, alias="date"),
    current_user=patient_permission(PermissionAction.VIEW),
    use_case: GetDailyFluidBalanceUseCase = Depends(
        FluidBalanceProvider.get_daily_use_case
    ),
) -> FluidBalanceSummaryResponse:
    """
    Return today's fluid balance summary (IN, OUT, BAL) for a patient.
    """
    summary = use_case.execute(patient_id=patient_id, target_date=target_date)
    return FluidBalanceSummaryResponse.model_validate(summary)
