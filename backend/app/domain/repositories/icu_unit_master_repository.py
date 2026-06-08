from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.icu_unit_master import ICUUnitMaster


class ICUUnitMasterRepository(ABC):
    """
    Domain repository interface for ICU unit management.
    """

    @abstractmethod
    def create(self, icu_unit: ICUUnitMaster) -> ICUUnitMaster:
        pass

    @abstractmethod
    def list(self) -> List[ICUUnitMaster]:
        pass

    @abstractmethod
    def by_id(self, icu_unit_id: int) -> Optional[ICUUnitMaster]:
        pass

    @abstractmethod
    def by_icu_name(self, icu_name: str) -> Optional[ICUUnitMaster]:
        pass

    @abstractmethod
    def exists_by_id(self, icu_unit_id: int) -> bool:
        pass

    @abstractmethod
    def exists_by_icu_name(self, icu_name: str) -> bool:
        pass

    @abstractmethod
    def exists_by_icu_name_except_id(
        self,
        icu_name: str,
        icu_unit_id: int,
    ) -> bool:
        pass

    @abstractmethod
    def update(self, icu_unit: ICUUnitMaster) -> ICUUnitMaster:
        pass

    @abstractmethod
    def delete(self, icu_unit_id: int) -> None:
        pass