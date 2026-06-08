# app/domain/repositories/latest_vital_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.latest_vital import LatestVital


class LatestVitalRepository(ABC):
    """
    Contract for latest patient vital snapshot persistence operations.
    """

    @abstractmethod
    def upsert(self, latest_vital: LatestVital) -> LatestVital:
        """
        Create or update the latest vital snapshot for a patient.

        A patient should have only one latest vital row.
        """
        pass

    @abstractmethod
    def get_by_patient_id(self, patient_id: int) -> Optional[LatestVital]:
        """
        Fetch latest vital snapshot for a patient.
        """
        pass

    @abstractmethod
    def list_by_patient_ids(
        self,
        patient_ids: List[int],
    ) -> dict[int, LatestVital]:
        """
        Fetch latest vital snapshots for multiple patients.
        """
        pass

    @abstractmethod
    def list_by_bed_ids(
        self,
        bed_ids: List[int],
    ) -> List[LatestVital]:
        """
        Fetch latest vital snapshots for multiple beds.
        """
        pass