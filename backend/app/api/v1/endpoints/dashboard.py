from typing import List

from fastapi import APIRouter, Depends, Query, status

from app.api.providers.auth import AuthProvider
from app.api.providers.dashboard import DashboardProvider
from app.api.schemas.dashboard import DashboardOverviewResponse
from app.api.schemas.icu_unit_master import ICUUnitMasterResponse
from app.application.dashboard.use_cases.get_dashboard_overview import (
    GetDashboardOverviewUseCase,
)
from app.application.dashboard.use_cases.list_dashboard_units import (
    ListDashboardUnitsUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


def dashboard_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for Dashboard routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.DASHBOARD,
            action,
        )
    )


@router.get(
    "/units",
    response_model=List[ICUUnitMasterResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_dashboard_units(
    _current_user=dashboard_permission(
        PermissionAction.VIEW
    ),
    use_case: ListDashboardUnitsUseCase = Depends(
        DashboardProvider.get_list_dashboard_units_use_case
    ),
) -> List[ICUUnitMasterResponse]:
    """
    Return ICU units available for dashboard selection.

    This endpoint uses DASHBOARD:VIEW permission instead of
    ICU_MANAGEMENT:VIEW, so clinical dashboard users can load
    unit options without needing admin privileges.
    """
    return use_case.execute()


@router.get(
    "/overview",
    response_model=DashboardOverviewResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_dashboard_overview(
    unit_id: int = Query(..., alias="unitId"),
    _current_user=dashboard_permission(
        PermissionAction.VIEW
    ),
    use_case: GetDashboardOverviewUseCase = Depends(
        DashboardProvider.get_dashboard_overview_use_case
    ),
) -> DashboardOverviewResponse:
    """
    Return aggregated ICU dashboard overview data.

    This endpoint powers:
    - bed-wise patient cards
    - latest vitals summary
    - monitoring device labels
    - critical alarm indicators
    - recent alarm feeds
    - ICU operational overview
    """
    return use_case.execute(unit_id=unit_id)