from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.schemas.report import ReportsResponse
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(prefix="/admin/reports", tags=["Admin - Reports"])


def reports_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.DASHBOARD,
            action,
        )
    )


@router.get(
    "",
    response_model=ReportsResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_reports(_current_user=reports_permission(PermissionAction.VIEW)):
    """
    Return mock reports data used by the frontend Reports page.
    """
    return {
        "reportCards": [
            {"title": "ICU Utilization", "desc": "Utilization rates across all ICU units"},
            {"title": "Bed Occupancy", "desc": "Bed occupancy trends and statistics"},
            {"title": "Device Downtime", "desc": "Device offline time and maintenance logs"},
            {"title": "Alert Frequency", "desc": "Alert patterns and severity distribution"},
            {"title": "Patient Monitoring", "desc": "Patient data flow and monitoring reports"},
        ],
        "icuData": [
            {"name": "General ICU", "value": 14},
            {"name": "Cardiac ICU", "value": 10},
            {"name": "Surgical ICU", "value": 7},
            {"name": "Pediatric ICU", "value": 6},
            {"name": "Neonatal ICU", "value": 12},
        ],
        "alertData": [
            {"time": "6 AM", "critical": 1, "warning": 3, "info": 5},
            {"time": "8 AM", "critical": 2, "warning": 4, "info": 3},
            {"time": "10 AM", "critical": 3, "warning": 2, "info": 4},
            {"time": "12 PM", "critical": 1, "warning": 5, "info": 2},
            {"time": "2 PM", "critical": 2, "warning": 3, "info": 6},
            {"time": "4 PM", "critical": 1, "warning": 4, "info": 3},
            {"time": "6 PM", "critical": 2, "warning": 2, "info": 4},
            {"time": "8 PM", "critical": 3, "warning": 3, "info": 2},
        ],
    }
