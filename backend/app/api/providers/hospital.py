from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.providers.db import DBProvider
from app.application.hospital.use_cases.create_hospital import CreateHospitalUseCase
from app.application.hospital.use_cases.create_hospital_unit import (
    CreateHospitalUnitUseCase,
)
from app.application.hospital.use_cases.get_hospital import GetHospitalUseCase
from app.application.hospital.use_cases.get_hospital_unit import GetHospitalUnitUseCase
from app.application.hospital.use_cases.list_hospitals import ListHospitalsUseCase
from app.application.hospital.use_cases.list_units_by_hospital import (
    ListUnitsByHospitalUseCase,
)
from app.infrastructure.repositories.sqlalchemy_hospital_repository import (
    SQLAlchemyHospitalRepository,
)


class HospitalProvider:
    """
    Provider class for hospital use case wiring.
    """

    @staticmethod
    def get_hospital_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyHospitalRepository:
        return SQLAlchemyHospitalRepository(db)

    @staticmethod
    def get_create_hospital_use_case(
        repository: SQLAlchemyHospitalRepository = Depends(
            get_hospital_repository
        ),
    ) -> CreateHospitalUseCase:
        return CreateHospitalUseCase(repository)

    @staticmethod
    def get_get_hospital_use_case(
        repository: SQLAlchemyHospitalRepository = Depends(
            get_hospital_repository
        ),
    ) -> GetHospitalUseCase:
        return GetHospitalUseCase(repository)

    @staticmethod
    def get_list_hospitals_use_case(
        repository: SQLAlchemyHospitalRepository = Depends(
            get_hospital_repository
        ),
    ) -> ListHospitalsUseCase:
        return ListHospitalsUseCase(repository)

    @staticmethod
    def get_create_hospital_unit_use_case(
        repository: SQLAlchemyHospitalRepository = Depends(
            get_hospital_repository
        ),
    ) -> CreateHospitalUnitUseCase:
        return CreateHospitalUnitUseCase(repository)

    @staticmethod
    def get_get_hospital_unit_use_case(
        repository: SQLAlchemyHospitalRepository = Depends(
            get_hospital_repository
        ),
    ) -> GetHospitalUnitUseCase:
        return GetHospitalUnitUseCase(repository)

    @staticmethod
    def get_list_units_by_hospital_use_case(
        repository: SQLAlchemyHospitalRepository = Depends(
            get_hospital_repository
        ),
    ) -> ListUnitsByHospitalUseCase:
        return ListUnitsByHospitalUseCase(repository)