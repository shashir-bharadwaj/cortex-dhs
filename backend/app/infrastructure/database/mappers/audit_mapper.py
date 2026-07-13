from typing import List

from app.domain.entities.audit import AuditLog
from app.infrastructure.database.models.audit import AuditLogModel


class AuditMapper:
    """
    Maps between AuditLog domain entity and SQLAlchemy model.
    """

    @staticmethod
    def to_domain(model: AuditLogModel) -> AuditLog:
        return AuditLog(
            id=model.id,
            timestamp=model.timestamp,
            user=model.user,
            role=model.role,
            action=model.action,
            module=model.module,
            ip_address=model.ip_address,
        )

    @staticmethod
    def to_model(domain: AuditLog) -> AuditLogModel:
        return AuditLogModel(
            id=domain.id,
            timestamp=domain.timestamp,
            user=domain.user,
            role=domain.role,
            action=domain.action,
            module=domain.module,
            ip_address=domain.ip_address,
        )

    @staticmethod
    def to_domain_list(models: List[AuditLogModel]) -> List[AuditLog]:
        return [AuditMapper.to_domain(model) for model in models]