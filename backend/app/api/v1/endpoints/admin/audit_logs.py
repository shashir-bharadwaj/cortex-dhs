from typing import List

from fastapi import APIRouter, Depends, status

from app.api.providers.admin.audit import AuditProvider
from app.api.providers.auth import AuthProvider
from app.api.schemas.audit_log import (
    AuditLogCreateRequest,
    AuditLogResponse,
    AuditLogUpdateRequest,
)
from app.application.audit.use_cases.create_audit import CreateAuditUseCase
from app.application.audit.use_cases.delete_audit import DeleteAuditUseCase
from app.application.audit.use_cases.list_audit import ListAuditsUseCase
from app.application.audit.use_cases.read_audit import ReadAuditUseCase
from app.application.audit.use_cases.update_audit import UpdateAuditUseCase
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(
    prefix="/admin/audits",
    tags=["Admin - Audit Management"],
)


def audit_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.BED_MANAGEMENT,
            action,
        )
    )


@router.post(
    "",
    response_model=AuditLogResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_audit(
    payload: AuditLogCreateRequest,
    _current_user=audit_permission(PermissionAction.CREATE),
    use_case: CreateAuditUseCase = Depends(
        AuditProvider.create_audit_use_case
    ),
):
    return use_case.execute(payload)


@router.get(
    "",
    response_model=List[AuditLogResponse],
    responses=STANDARD_ERROR_RESPONSES,
)
def list_audits(
    _current_user=audit_permission(PermissionAction.VIEW),
    use_case: ListAuditsUseCase = Depends(
        AuditProvider.list_audits_use_case
    ),
):
    return use_case.execute()


@router.get(
    "/{audit_id}",
    response_model=AuditLogResponse,
    responses=STANDARD_ERROR_RESPONSES,
)
def read_audit(
    audit_id: int,
    _current_user=audit_permission(PermissionAction.VIEW),
    use_case: ReadAuditUseCase = Depends(
        AuditProvider.read_audit_use_case
    ),
):
    return use_case.execute(audit_id)


@router.put(
    "/{audit_id}",
    response_model=AuditLogResponse,
    responses=STANDARD_ERROR_RESPONSES,
)
def update_audit(
    audit_id: int,
    payload: AuditLogUpdateRequest,
    _current_user=audit_permission(PermissionAction.MODIFY),
    use_case: UpdateAuditUseCase = Depends(
        AuditProvider.update_audit_use_case
    ),
):
    return use_case.execute(audit_id, payload)


@router.delete(
    "/{audit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=STANDARD_ERROR_RESPONSES,
)
def delete_audit(
    audit_id: int,
    _current_user=audit_permission(PermissionAction.DELETE),
    use_case: DeleteAuditUseCase = Depends(
        AuditProvider.delete_audit_use_case
    ),
):
    use_case.execute(audit_id)
    return None