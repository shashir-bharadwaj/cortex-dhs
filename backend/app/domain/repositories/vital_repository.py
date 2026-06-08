# app/domain/repositories/vital_repository.py

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from app.domain.entities.vital import Vital


class VitalRepository(ABC):
    """
    Contract for vital persistence operations.
    """

    @abstractmethod
    def create(self, vital: Vital) -> Vital:
        pass

    @abstractmethod
    def get_by_id(self, vital_id: int) -> Optional[Vital]:
        pass

    @abstractmethod
    def list_by_patient_id(self, patient_id: int) -> List[Vital]:
        pass

    @abstractmethod
    def list_latest_by_patient_id(self, patient_id: int, limit: int = 20) -> List[Vital]:
        pass

    @abstractmethod
    def list_latest_for_patients(
        self,
        patient_ids: List[int],
    ) -> Dict[int, list[Vital]]:
        """
        Fetch latest vitals grouped by patient id.
        """
        raise NotImplementedError
    
    @abstractmethod
    def create_from_ingestion(
        self,
        data: dict,
    ) -> Vital:
        pass