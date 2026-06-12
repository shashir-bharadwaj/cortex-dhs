from abc import ABC, abstractmethod
from datetime import date
from typing import List

from app.domain.entities.fluid_balance import FluidBalance


class FluidBalanceRepository(ABC):
    """
    Domain repository contract for fluid balance records.
    """

    @abstractmethod
    def create(self, record: FluidBalance) -> FluidBalance:
        pass

    @abstractmethod
    def list_by_patient_id_and_date(
        self, patient_id: int, target_date: date
    ) -> List[FluidBalance]:
        pass

    @abstractmethod
    def list_by_patient_id(self, patient_id: int) -> List[FluidBalance]:
        pass
