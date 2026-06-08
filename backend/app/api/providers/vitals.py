from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.vitals.use_cases.create_vital import CreateVitalUseCase
from app.application.vitals.use_cases.get_vital import GetVitalUseCase
from app.application.vitals.use_cases.list_patient_vitals import ListPatientVitalsUseCase
from app.infrastructure.repositories.sqlalchemy_patient_repository import (
    SQLAlchemyPatientRepository,
)
from app.infrastructure.repositories.sqlalchemy_vital_repository import (
    SQLAlchemyVitalRepository,
)


class VitalProvider:
    """
    Provider class responsible for constructing
    all Vital-related application use cases.

    Why this exists:
    ----------------
    Keeps route files thin and focused on:
    - request parsing
    - response formatting
    - HTTP error handling

    while moving dependency wiring here.
    """

    @staticmethod
    def get_create_vital_use_case(
        # Repository used to persist new vital records
        vital_repository: SQLAlchemyVitalRepository = Depends(
            RepositoryProvider.get_vital_repository
        ),
        # Repository used to validate patient existence
        patient_repository: SQLAlchemyPatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> CreateVitalUseCase:
        """
        Build the use case for creating a vital record.

        This use case depends on:
        - patient repository: ensures patient exists
        - vital repository: saves the record
        """
        return CreateVitalUseCase(
            vital_repository=vital_repository,
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_get_vital_use_case(
        # Repository used to fetch a single vital record
        vital_repository: SQLAlchemyVitalRepository = Depends(
            RepositoryProvider.get_vital_repository
        ),
    ) -> GetVitalUseCase:
        """
        Build the use case for fetching
        a single vital record by ID.
        """
        return GetVitalUseCase(vital_repository)

    @staticmethod
    def get_list_patient_vitals_use_case(
        # Repository used to fetch patient vital history
        vital_repository: SQLAlchemyVitalRepository = Depends(
            RepositoryProvider.get_vital_repository
        ),
        # Repository used to validate patient existence first
        patient_repository: SQLAlchemyPatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> ListPatientVitalsUseCase:
        """
        Build the use case for listing
        all vitals for a given patient.

        Why patient repository is needed:
        ---------------------------------
        We first confirm the patient exists
        before returning their vital history.
        """
        return ListPatientVitalsUseCase(
            vital_repository=vital_repository,
            patient_repository=patient_repository,
        )