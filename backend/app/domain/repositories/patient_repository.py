from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.patient import Patient


class PatientRepository(ABC):
    """
    Domain repository interface for patient operations.

    Application use cases depend on this abstraction,
    not on SQLAlchemy implementations.
    """

    @abstractmethod
    def create(
        self,
        patient: Patient,
    ) -> Patient:
        pass

    @abstractmethod
    def list(self) -> List[Patient]:
        pass

    @abstractmethod
    def by_id(
        self,
        patient_id: int,
    ) -> Optional[Patient]:
        pass

    @abstractmethod
    def update(
        self,
        patient: Patient,
    ) -> Patient:
        pass

    @abstractmethod
    def discharge(
        self,
        patient_id: int,
    ) -> Optional[Patient]:
        pass

    @abstractmethod
    def get_active_by_bed_id(
        self,
        bed_id: int,
    ) -> Optional[Patient]:
        pass

    @abstractmethod
    def list_active_by_bed_ids(
        self,
        bed_ids: List[int],
    ) -> List[Patient]:
        pass