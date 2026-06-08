from fastapi import APIRouter, Depends, Query, status

from app.api.providers.auth import AuthProvider
from app.api.providers.dashboard import DashboardProvider
from app.api.schemas.dashboard import DashboardOverviewResponse
from app.application.dashboard.use_cases.get_dashboard_overview import (
    GetDashboardOverviewUseCase,
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