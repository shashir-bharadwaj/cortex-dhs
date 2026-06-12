from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.medication.use_cases.create_medication_order import (
    CreateMedicationOrderUseCase,
)
from app.application.medication.use_cases.list_medication_orders import (
    ListMedicationOrdersUseCase,
)
from app.domain.repositories.medication_order_repository import MedicationOrderRepository
from app.domain.repositories.patient_repository import PatientRepository


class MedicationOrderProvider:
    """
    Provider for Medication Order use cases.
    """

    @staticmethod
    def get_create_use_case(
        medication_order_repository: MedicationOrderRepository = Depends(
            RepositoryProvider.get_medication_order_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> CreateMedicationOrderUseCase:
        return CreateMedicationOrderUseCase(
            medication_order_repository=medication_order_repository,
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_list_use_case(
        medication_order_repository: MedicationOrderRepository = Depends(
            RepositoryProvider.get_medication_order_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> ListMedicationOrdersUseCase:
        return ListMedicationOrdersUseCase(
            medication_order_repository=medication_order_repository,
            patient_repository=patient_repository,
        )
