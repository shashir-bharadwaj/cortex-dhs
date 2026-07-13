from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.providers.auth import AuthProvider
from app.api.schemas.cloud_sync import CloudSyncResponse
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.db.database import get_db
from app.domain.enums.permission import PermissionAction, PermissionModule
from app.infrastructure.database.models.hospital import HospitalModel

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
def get_cloudsync_status(
    _current_user=cloudsync_permission(PermissionAction.VIEW),
    db: Session = Depends(get_db),
):
    """
    Return cloud sync status from database.
    """

    hospitals = db.query(HospitalModel).all()

    hospital_payload = []

    connected = 0

    for hospital in hospitals:

       


        hospital_payload.append(
            {
                "id": hospital.id,
                "name": hospital.name,
                "city": hospital.city,
                "status": "",
                "lastSync": "Just now",
                "data": "N/A",
            }
        )

    return {
        "summary": {
            "lastSync": datetime.utcnow().strftime("%I:%M %p"),
            "dataSent": "N/A",
            "errors": 0,
            "hospitals": connected,
        },
        "hospitals": hospital_payload,
    }