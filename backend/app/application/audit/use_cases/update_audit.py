from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.audit import AuditLog
from app.domain.repositories.audit_repository import AuditRepository


class UpdateAuditUseCase:
    """
    Use case for updating an audit log.
    """

    def __init__(self, audit_repository: AuditRepository):
        self.audit_repository = audit_repository

    def execute(self, audit_id: int, payload) -> AuditLog:
        audit = self.audit_repository.by_id(audit_id)

        if audit is None:
            raise ResourceNotFoundError(
                message="Audit log not found.",
                meta={"id": audit_id},
            )

        audit.timestamp = payload.timestamp
        audit.user = payload.user
        audit.role = payload.role
        audit.action = payload.action
        audit.module = payload.module
        audit.ip_address = payload.ip_address

        return self.audit_repository.update(audit)