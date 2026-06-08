from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.bed import BedMaster


class BedRepository(ABC):
    """
    Domain repository interface for bed management.

    Application use cases depend on this abstraction, not directly on SQLAlchemy.
    """

    @abstractmethod
    def create(self, bed: BedMaster) -> BedMaster:
        pass

    @abstractmethod
    def list(self) -> List[BedMaster]:
        pass

    @abstractmethod
    def list_by_icu_unit_id(self, icu_unit_id: int) -> List[BedMaster]:
        pass

    @abstractmethod
    def by_id(self, id: int) -> Optional[BedMaster]:
        pass

    @abstractmethod
    def by_bed_id(self, bed_id: str) -> Optional[BedMaster]:
        pass

    @abstractmethod
    def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    def exists_by_bed_id(self, bed_id: str) -> bool:
        pass

    @abstractmethod
    def exists_by_bed_id_except_id(self, bed_id: str, id: int) -> bool:
        pass

    @abstractmethod
    def update(self, bed: BedMaster) -> BedMaster:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

    @abstractmethod
    def get_by_bed_id(
        self,
        bed_id: str,
    ) -> Optional[BedMaster]:
        pass