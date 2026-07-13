from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.audit_repository import AuditRepository


class DeleteAuditUseCase:
    """
    Use case for deleting an audit log.
    """

    def __init__(self, audit_repository: AuditRepository):
        self.audit_repository = audit_repository

    def execute(self, audit_id: int) -> None:
        audit = self.audit_repository.by_id(audit_id)

        if audit is None:
            raise ResourceNotFoundError(
                message="Audit log not found.",
                meta={"id": audit_id},
            )

        self.audit_repository.delete(audit_id)