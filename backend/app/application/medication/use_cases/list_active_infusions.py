from typing import List

from app.domain.entities.medication_order import MedicationOrder
from app.domain.repositories.medication_order_repository import MedicationOrderRepository


class ListActiveInfusionsUseCase:

    def __init__(self, medication_order_repository: MedicationOrderRepository):
        self.medication_order_repository = medication_order_repository

    def execute(self) -> List[MedicationOrder]:
        return self.medication_order_repository.list_all_active_infusions()
