from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.audit import AuditLog


class AuditRepository(ABC):
    """
    Domain repository interface for audit log management.
    """

    @abstractmethod
    def create(self, audit: AuditLog) -> AuditLog:
        pass

    @abstractmethod
    def list(self) -> List[AuditLog]:
        pass

    @abstractmethod
    def by_id(self, id: int) -> Optional[AuditLog]:
        pass

    @abstractmethod
    def update(self, audit: AuditLog) -> AuditLog:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass