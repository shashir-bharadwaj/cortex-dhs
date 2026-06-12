from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.medication_order import MedicationOrder


class MedicationOrderRepository(ABC):
    """
    Domain repository contract for medication orders.
    """

    @abstractmethod
    def create(self, order: MedicationOrder) -> MedicationOrder:
        pass

    @abstractmethod
    def list_by_patient_id(self, patient_id: int) -> List[MedicationOrder]:
        pass

    @abstractmethod
    def list_active_infusions_by_patient_id(
        self, patient_id: int
    ) -> List[MedicationOrder]:
        pass

    @abstractmethod
    def by_id(self, order_id: int) -> Optional[MedicationOrder]:
        pass

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> Optional[MedicationOrder]:
        pass
