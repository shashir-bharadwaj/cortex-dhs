from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.providers.db import DBProvider
from app.application.bed_management.use_cases.create_bed import CreateBedUseCase
from app.application.bed_management.use_cases.delete_bed import DeleteBedUseCase
from app.application.bed_management.use_cases.list_beds import ListBedsUseCase
from app.application.bed_management.use_cases.read_bed import ReadBedUseCase
from app.application.bed_management.use_cases.update_bed import UpdateBedUseCase
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.icu_unit_master_repository import (
    ICUUnitMasterRepository,
)
from app.infrastructure.repositories.sqlalchemy_bed_repository import (
    SQLAlchemyBedRepository,
)
from app.infrastructure.repositories.sqlalchemy_icu_unit_master_repository import (
    SQLAlchemyICUUnitMasterRepository,
)


class BedManagementProvider:
    """
    Provider for bed management dependencies.

    Provider layer wires infrastructure implementations
    to domain repository abstractions.
    """

    @staticmethod
    def bed_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> BedRepository:
        return SQLAlchemyBedRepository(db)

    @staticmethod
    def icu_unit_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> ICUUnitMasterRepository:
        return SQLAlchemyICUUnitMasterRepository(db)

    @staticmethod
    def create_bed_use_case(
        bed_repository: BedRepository = Depends(bed_repository),
        icu_unit_repository: ICUUnitMasterRepository = Depends(
            icu_unit_repository
        ),
    ) -> CreateBedUseCase:
        return CreateBedUseCase(
            bed_repository=bed_repository,
            icu_unit_repository=icu_unit_repository,
        )

    @staticmethod
    def list_beds_use_case(
        repository: BedRepository = Depends(bed_repository),
    ) -> ListBedsUseCase:
        return ListBedsUseCase(repository)

    @staticmethod
    def read_bed_use_case(
        repository: BedRepository = Depends(bed_repository),
    ) -> ReadBedUseCase:
        return ReadBedUseCase(repository)

    @staticmethod
    def update_bed_use_case(
        bed_repository: BedRepository = Depends(bed_repository),
        icu_unit_repository: ICUUnitMasterRepository = Depends(
            icu_unit_repository
        ),
    ) -> UpdateBedUseCase:
        return UpdateBedUseCase(
            bed_repository=bed_repository,
            icu_unit_repository=icu_unit_repository,
        )

    @staticmethod
    def delete_bed_use_case(
        repository: BedRepository = Depends(bed_repository),
    ) -> DeleteBedUseCase:
        return DeleteBedUseCase(repository)