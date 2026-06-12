from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.lab_result import LabResult


class LabResultRepository(ABC):
    """
    Domain repository contract for lab results.
    """

    @abstractmethod
    def create(self, result: LabResult) -> LabResult:
        pass

    @abstractmethod
    def get_latest_by_patient_id(self, patient_id: int) -> Optional[LabResult]:
        pass

    @abstractmethod
    def list_by_patient_id(self, patient_id: int) -> List[LabResult]:
        pass
