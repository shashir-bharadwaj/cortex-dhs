from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.lab_results.use_cases.create_lab_result import CreateLabResultUseCase
from app.application.lab_results.use_cases.get_latest_lab_result import GetLatestLabResultUseCase
from app.domain.repositories.lab_result_repository import LabResultRepository
from app.domain.repositories.patient_repository import PatientRepository


class LabResultProvider:
    """
    Provider for Lab Result use cases.
    """

    @staticmethod
    def get_create_use_case(
        lab_result_repository: LabResultRepository = Depends(
            RepositoryProvider.get_lab_result_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> CreateLabResultUseCase:
        return CreateLabResultUseCase(
            lab_result_repository=lab_result_repository,
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_latest_use_case(
        lab_result_repository: LabResultRepository = Depends(
            RepositoryProvider.get_lab_result_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> GetLatestLabResultUseCase:
        return GetLatestLabResultUseCase(
            lab_result_repository=lab_result_repository,
            patient_repository=patient_repository,
        )
