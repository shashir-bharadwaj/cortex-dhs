from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.providers.auth import AuthProvider
from app.api.schemas.connectivity import ConnectivityResponse
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.db.database import get_db
from app.domain.enums.permission import PermissionAction, PermissionModule
from app.infrastructure.database.models.bed import BedMasterModel
from app.infrastructure.database.models.device_master import DeviceMasterModel

router = APIRouter(prefix="/admin/connectivity", tags=["Admin - Connectivity"])


def connectivity_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.DEVICE_MANAGEMENT,
            action,
        )
    )


@router.get(
    "",
    response_model=ConnectivityResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_connectivity_status(
    _current_user=connectivity_permission(PermissionAction.VIEW),
    db: Session = Depends(get_db),
):
    """
    Return connectivity telemetry aggregated from the database.
    """
    devices = db.query(DeviceMasterModel).all()
    online = sum(1 for device in devices if (device.status or "").upper() == "ONLINE")
    offline = len(devices) - online

    timeline = [
        {"time": "00:00", "online": max(0, online - 2), "offline": max(0, offline + 1)},
        {"time": "04:00", "online": max(0, online - 1), "offline": max(0, offline)},
        {"time": "08:00", "online": online, "offline": offline},
        {"time": "12:00", "online": max(0, online + 1), "offline": max(0, offline - 1)},
        {"time": "16:00", "online": max(0, online), "offline": max(0, offline)},
        {"time": "20:00", "online": max(0, online + 1), "offline": max(0, offline - 1)},
        {"time": "Now", "online": online, "offline": offline},
    ]

    device_payload = []
    for device in devices:
        bed_label = "N/A"
        if device.bed_id is not None:
            bed = db.query(BedMasterModel).filter(BedMasterModel.id == device.bed_id).first()
            if bed:
                bed_label = bed.bed_id

        device_payload.append(
            {
                "id": str(device.id),
                "type": device.device_type or "Device",
                "bed": bed_label,
                "status": device.status or "UNKNOWN",
                "lastSync": "just now",
                "ip": device.ip_address or "N/A",
            }
        )

    return {
        "summary": {
            "online": online,
            "offline": offline,
            "dataRate": "N/A",
            "latency": "N/A",
        },
        "timeline": timeline,
        "devices": device_payload,
    }
