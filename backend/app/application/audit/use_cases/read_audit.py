from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.audit import AuditLog
from app.domain.repositories.audit_repository import AuditRepository


class ReadAuditUseCase:
    """
    Use case for reading a single audit log by ID.
    """

    def __init__(self, audit_repository: AuditRepository):
        self.audit_repository = audit_repository

    def execute(self, audit_id: int) -> AuditLog:
        audit = self.audit_repository.by_id(audit_id)

        if audit is None:
            raise ResourceNotFoundError(
                message="Audit log not found.",
                meta={"id": audit_id},
            )

        return audit