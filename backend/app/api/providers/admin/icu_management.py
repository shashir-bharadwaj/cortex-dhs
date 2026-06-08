from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.providers.db import DBProvider
from app.application.icu_management.use_cases.create_icu_unit import CreateICUUnitUseCase
from app.application.icu_management.use_cases.delete_icu_unit import DeleteICUUnitUseCase
from app.application.icu_management.use_cases.list_icu_units import ListICUUnitsUseCase
from app.application.icu_management.use_cases.read_icu_unit import ReadICUUnitUseCase
from app.application.icu_management.use_cases.update_icu_unit import UpdateICUUnitUseCase
from app.infrastructure.repositories.sqlalchemy_icu_unit_master_repository import (
    SQLAlchemyICUUnitMasterRepository,
)


class ICUManagementProvider:
    """
    Provider for ICU management dependencies.
    """

    @staticmethod
    def icu_unit_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyICUUnitMasterRepository:
        return SQLAlchemyICUUnitMasterRepository(db)

    @staticmethod
    def create_icu_unit_use_case(
        repository: SQLAlchemyICUUnitMasterRepository = Depends(icu_unit_repository),
    ) -> CreateICUUnitUseCase:
        return CreateICUUnitUseCase(repository)

    @staticmethod
    def list_icu_units_use_case(
        repository: SQLAlchemyICUUnitMasterRepository = Depends(icu_unit_repository),
    ) -> ListICUUnitsUseCase:
        return ListICUUnitsUseCase(repository)

    @staticmethod
    def read_icu_unit_use_case(
        repository: SQLAlchemyICUUnitMasterRepository = Depends(icu_unit_repository),
    ) -> ReadICUUnitUseCase:
        return ReadICUUnitUseCase(repository)

    @staticmethod
    def update_icu_unit_use_case(
        repository: SQLAlchemyICUUnitMasterRepository = Depends(icu_unit_repository),
    ) -> UpdateICUUnitUseCase:
        return UpdateICUUnitUseCase(repository)

    @staticmethod
    def delete_icu_unit_use_case(
        repository: SQLAlchemyICUUnitMasterRepository = Depends(icu_unit_repository),
    ) -> DeleteICUUnitUseCase:
        return DeleteICUUnitUseCase(repository)