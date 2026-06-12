from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.fluid_balance.use_cases.create_fluid_balance_record import (
    CreateFluidBalanceRecordUseCase,
)
from app.application.fluid_balance.use_cases.get_daily_fluid_balance import (
    GetDailyFluidBalanceUseCase,
)
from app.domain.repositories.fluid_balance_repository import FluidBalanceRepository
from app.domain.repositories.patient_repository import PatientRepository


class FluidBalanceProvider:
    """
    Provider for Fluid Balance use cases.
    """

    @staticmethod
    def get_create_use_case(
        fluid_balance_repository: FluidBalanceRepository = Depends(
            RepositoryProvider.get_fluid_balance_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> CreateFluidBalanceRecordUseCase:
        return CreateFluidBalanceRecordUseCase(
            fluid_balance_repository=fluid_balance_repository,
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_daily_use_case(
        fluid_balance_repository: FluidBalanceRepository = Depends(
            RepositoryProvider.get_fluid_balance_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> GetDailyFluidBalanceUseCase:
        return GetDailyFluidBalanceUseCase(
            fluid_balance_repository=fluid_balance_repository,
            patient_repository=patient_repository,
        )
