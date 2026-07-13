from typing import List

from app.domain.entities.audit import AuditLog
from app.domain.repositories.audit_repository import AuditRepository


class ListAuditsUseCase:
    """
    Use case for listing audit logs.
    """

    def __init__(self, audit_repository: AuditRepository):
        self.audit_repository = audit_repository

    def execute(self) -> List[AuditLog]:
        return self.audit_repository.list()