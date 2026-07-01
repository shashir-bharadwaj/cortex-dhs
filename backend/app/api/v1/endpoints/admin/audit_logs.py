from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.schemas.audit_log import AuditLogResponse
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(
    prefix="/admin/audit-logs",
    tags=["Admin - Audit Logs"],
)


def audit_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.DEVICE_MANAGEMENT,
            action,
        )
    )


@router.get(
    "",
    response_model=list[AuditLogResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_audit_logs(
    _current_user=audit_permission(PermissionAction.VIEW),
):
    """
    Return mock audit log entries for the admin console.
    """
    return [
        AuditLogResponse(
            id=1,
            time="2026-06-30 10:42:00",
            user="Dr. Sarah Chen",
            role="Admin",
            action="Acknowledged critical alert ALT-001",
            module="Alerts",
            ip="192.168.0.15",
        ),
        AuditLogResponse(
            id=2,
            time="2026-06-30 10:38:00",
            user="Tom Baker",
            role="Technician",
            action="Ran diagnostics on Ventilator DEV-007",
            module="Device Management",
            ip="192.168.0.22",
        ),
        AuditLogResponse(
            id=3,
            time="2026-06-30 10:20:00",
            user="Dr. Sarah Chen",
            role="Admin",
            action="Registered new ventilator DEV-011",
            module="Device Management",
            ip="192.168.0.15",
        ),
        AuditLogResponse(
            id=4,
            time="2026-06-30 10:05:00",
            user="Kevin Lee",
            role="Hospital IT",
            action="Updated network gateway GW-02",
            module="ICU Management",
            ip="192.168.0.30",
        ),
        AuditLogResponse(
            id=5,
            time="2026-06-30 09:50:00",
            user="Dr. Sarah Chen",
            role="Admin",
            action="Created user account for Dr. Patel",
            module="User Management",
            ip="192.168.0.15",
        ),
    ]
