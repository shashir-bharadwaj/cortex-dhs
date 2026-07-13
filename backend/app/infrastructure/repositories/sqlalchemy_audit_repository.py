from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.audit import AuditLog
from app.domain.repositories.audit_repository import AuditRepository
from app.infrastructure.database.mappers.audit_mapper import AuditMapper
from app.infrastructure.database.models.audit import AuditLogModel


class SQLAlchemyAuditRepository(AuditRepository):
    """
    SQLAlchemy implementation of AuditRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, audit: AuditLog) -> AuditLog:
        model = AuditMapper.to_model(audit)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return AuditMapper.to_domain(model)

    def list(self) -> List[AuditLog]:
        models = (
            self.db.query(AuditLogModel)
            .order_by(AuditLogModel.timestamp.desc())
            .all()
        )

        return AuditMapper.to_domain_list(models)

    def by_id(self, id: int) -> Optional[AuditLog]:
        model = (
            self.db.query(AuditLogModel)
            .filter(AuditLogModel.id == id)
            .first()
        )

        if not model:
            return None

        return AuditMapper.to_domain(model)

    def update(self, audit: AuditLog) -> AuditLog:
        model = (
            self.db.query(AuditLogModel)
            .filter(AuditLogModel.id == audit.id)
            .first()
        )

        model.timestamp = audit.timestamp
        model.user = audit.user
        model.role = audit.role
        model.action = audit.action
        model.module = audit.module
        model.ip_address = audit.ip_address

        self.db.commit()
        self.db.refresh(model)

        return AuditMapper.to_domain(model)

    def delete(self, id: int) -> None:
        model = (
            self.db.query(AuditLogModel)
            .filter(AuditLogModel.id == id)
            .first()
        )

        if model:
            self.db.delete(model)
            self.db.commit()