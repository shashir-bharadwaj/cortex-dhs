from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.ventilator.use_cases.create_ventilator_setting import (
    CreateVentilatorSettingUseCase,
)
from app.application.ventilator.use_cases.get_latest_ventilator_setting import (
    GetLatestVentilatorSettingUseCase,
)
from app.domain.repositories.patient_repository import PatientRepository
from app.domain.repositories.ventilator_setting_repository import VentilatorSettingRepository


class VentilatorSettingProvider:
    """
    Provider for Ventilator Setting use cases.
    """

    @staticmethod
    def get_create_use_case(
        ventilator_repository: VentilatorSettingRepository = Depends(
            RepositoryProvider.get_ventilator_setting_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> CreateVentilatorSettingUseCase:
        return CreateVentilatorSettingUseCase(
            ventilator_repository=ventilator_repository,
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_latest_use_case(
        ventilator_repository: VentilatorSettingRepository = Depends(
            RepositoryProvider.get_ventilator_setting_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> GetLatestVentilatorSettingUseCase:
        return GetLatestVentilatorSettingUseCase(
            ventilator_repository=ventilator_repository,
            patient_repository=patient_repository,
        )
