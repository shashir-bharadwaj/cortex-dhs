from app.domain.entities.audit import AuditLog
from app.domain.repositories.audit_repository import AuditRepository


class CreateAuditUseCase:
    """
    Use case for creating an audit log.
    """

    def __init__(self, audit_repository: AuditRepository):
        self.audit_repository = audit_repository

    def execute(self, payload) -> AuditLog:
        audit = AuditLog(
            id=None,
            timestamp=payload.timestamp,
            user=payload.user,
            role=payload.role,
            action=payload.action,
            module=payload.module,
            ip_address=payload.ip_address,
        )

        return self.audit_repository.create(audit)