from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.schemas.settings import SettingsPayload, SettingsResponse
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(prefix="/admin/settings", tags=["Admin - Settings"])


def settings_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.DEVICE_MANAGEMENT,
            action,
        )
    )


@router.get(
    "",
    response_model=SettingsResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_settings(_current_user=settings_permission(PermissionAction.VIEW)):
    """
    Return mock system settings based on the frontend Settings page.
    """
    return {
        "hospitalName": "Metro General Hospital",
        "adminEmail": "admin@metrogeneral.com",
        "settings": {
            "realTimeAlerts": True,
            "autoSync": True,
            "autoDiscovery": False,
        },
    }


@router.post(
    "",
    response_model=SettingsResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def save_settings(payload: SettingsPayload, _current_user=settings_permission(PermissionAction.CREATE)):
    """
    Accept system settings from the frontend and echo them back as the saved state.
    """
    return {
        "hospitalName": payload.hospital_name,
        "adminEmail": payload.admin_email,
        "settings": payload.settings,
    }
