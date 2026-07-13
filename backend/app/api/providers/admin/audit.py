from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.audit.use_cases.create_audit import CreateAuditUseCase
from app.application.audit.use_cases.delete_audit import DeleteAuditUseCase
from app.application.audit.use_cases.list_audit import ListAuditsUseCase
from app.application.audit.use_cases.read_audit import ReadAuditUseCase
from app.application.audit.use_cases.update_audit import UpdateAuditUseCase
from app.db.database import get_db
from app.infrastructure.repositories.sqlalchemy_audit_repository import (
    SQLAlchemyAuditRepository,
)


class AuditProvider:

    @staticmethod
    def audit_repository(
        db: Session = Depends(get_db),
    ):
        return SQLAlchemyAuditRepository(db)

    @staticmethod
    def create_audit_use_case(
        repository=Depends(audit_repository),
    ):
        return CreateAuditUseCase(repository)

    @staticmethod
    def list_audits_use_case(
        repository=Depends(audit_repository),
    ):
        return ListAuditsUseCase(repository)

    @staticmethod
    def read_audit_use_case(
        repository=Depends(audit_repository),
    ):
        return ReadAuditUseCase(repository)

    @staticmethod
    def update_audit_use_case(
        repository=Depends(audit_repository),
    ):
        return UpdateAuditUseCase(repository)

    @staticmethod
    def delete_audit_use_case(
        repository=Depends(audit_repository),
    ):
        return DeleteAuditUseCase(repository)