from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.clinical_note import ClinicalNote


class ClinicalNoteRepository(ABC):
    """
    Domain repository contract for clinical notes.
    """

    @abstractmethod
    def create(
        self,
        note: ClinicalNote,
    ) -> ClinicalNote:
        pass

    @abstractmethod
    def list_by_patient_id(
        self,
        patient_id: int,
    ) -> List[ClinicalNote]:
        pass

    @abstractmethod
    def by_id(
        self,
        note_id: int,
    ) -> Optional[ClinicalNote]:
        pass

    @abstractmethod
    def delete(
        self,
        note_id: int,
    ) -> None:
        pass