from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.schemas.connectivity import ConnectivityResponse
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

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
def get_connectivity_status(_current_user=connectivity_permission(PermissionAction.VIEW)):
    """
    Return mock connectivity telemetry based on the frontend connectivity context.
    """
    return {
        "summary": {
            "online": 7,
            "offline": 3,
            "dataRate": "1.2 Gbps",
            "latency": "12ms",
        },
        "timeline": [
            {"time": "00:00", "online": 235, "offline": 20},
            {"time": "04:00", "online": 234, "offline": 22},
            {"time": "08:00", "online": 238, "offline": 15},
            {"time": "12:00", "online": 240, "offline": 10},
            {"time": "16:00", "online": 238, "offline": 12},
            {"time": "20:00", "online": 237, "offline": 14},
            {"time": "Now", "online": 239, "offline": 13},
        ],
        "devices": [
            {
                "id": "DEV-001",
                "type": "Patient Monitor",
                "bed": "ICU-C-01",
                "status": "Online",
                "lastSync": "30 sec ago",
                "ip": "192.168.1.101",
            },
            {
                "id": "DEV-002",
                "type": "Ventilator",
                "bed": "ICU-C-01",
                "status": "Online",
                "lastSync": "1 min ago",
                "ip": "192.168.1.102",
            },
            {
                "id": "DEV-003",
                "type": "ECG Monitor",
                "bed": "ICU-C-02",
                "status": "Online",
                "lastSync": "45 sec ago",
                "ip": "192.168.1.103",
            },
            {
                "id": "DEV-004",
                "type": "Infusion Pump",
                "bed": "ICU-C-02",
                "status": "Online",
                "lastSync": "2 min ago",
                "ip": "192.168.1.104",
            },
            {
                "id": "DEV-005",
                "type": "SpO2 Monitor",
                "bed": "ICU-C-03",
                "status": "Offline",
                "lastSync": "25 min ago",
                "ip": "192.168.1.105",
            },
            {
                "id": "DEV-006",
                "type": "Temperature Monitor",
                "bed": "ICU-G-01",
                "status": "Online",
                "lastSync": "1 min ago",
                "ip": "192.168.1.106",
            },
            {
                "id": "DEV-007",
                "type": "Ventilator",
                "bed": "ICU-G-03",
                "status": "Error",
                "lastSync": "15 min ago",
                "ip": "192.168.1.107",
            },
            {
                "id": "DEV-008",
                "type": "Patient Monitor",
                "bed": "ICU-N-01",
                "status": "Online",
                "lastSync": "20 sec ago",
                "ip": "192.168.1.108",
            },
            {
                "id": "DEV-009",
                "type": "ECG Monitor",
                "bed": "ICU-S-01",
                "status": "Online",
                "lastSync": "40 sec ago",
                "ip": "192.168.1.109",
            },
        ],
    }
