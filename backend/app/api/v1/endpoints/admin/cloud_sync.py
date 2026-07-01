from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.schemas.cloud_sync import (
    CloudSyncResponse,
    CloudSyncTriggerResponse,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(prefix="/admin/cloudsync", tags=["Admin - Cloud Sync"])


def cloudsync_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.DEVICE_MANAGEMENT,
            action,
        )
    )


@router.get(
    "",
    response_model=CloudSyncResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_cloudsync_status(_current_user=cloudsync_permission(PermissionAction.VIEW)):
    """
    Return mock cloud sync status.
    """
    return {
        "summary": {
            "lastSync": "2 min ago",
            "dataSent": "2.74 GB",
            "errors": 1,
            "hospitals": 3,
        },
        "hospitals": [
            {
                "id": 1,
                "name": "Metro General Hospital",
                "city": "New York",
                "status": "Connected",
                "lastSync": "2 min ago",
                "data": "1.2 GB",
            },
            {
                "id": 2,
                "name": "St. Mary's Medical Center",
                "city": "Chicago",
                "status": "Connected",
                "lastSync": "5 min ago",
                "data": "890 MB",
            },
            {
                "id": 3,
                "name": "Pacific Health Institute",
                "city": "San Francisco",
                "status": "Delayed",
                "lastSync": "25 min ago",
                "data": "650 MB",
            },
        ],
    }


@router.post(
    "/trigger",
    response_model=CloudSyncTriggerResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses=STANDARD_ERROR_RESPONSES,
)
def trigger_cloudsync(_current_user=cloudsync_permission(PermissionAction.CREATE)):
    """
    Trigger a cloud sync operation (mock implementation).
    """
    return CloudSyncTriggerResponse(started=True, message="Cloud sync started (mock)")
