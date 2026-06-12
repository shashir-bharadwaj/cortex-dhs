from typing import List

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.medication_order import MedicationOrder
from app.domain.repositories.medication_order_repository import MedicationOrderRepository
from app.domain.repositories.patient_repository import PatientRepository


class ListMedicationOrdersUseCase:
    """
    Return all medication orders for a patient.
    """

    def __init__(
        self,
        medication_order_repository: MedicationOrderRepository,
        patient_repository: PatientRepository,
    ):
        self.medication_order_repository = medication_order_repository
        self.patient_repository = patient_repository

    def execute(self, patient_id: int) -> List[MedicationOrder]:
        patient = self.patient_repository.by_id(patient_id)
        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )
        return self.medication_order_repository.list_by_patient_id(patient_id)
