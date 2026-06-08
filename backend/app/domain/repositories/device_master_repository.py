from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from app.domain.entities.device_master import DeviceMaster


class DeviceMasterRepository(ABC):
    """
    Domain repository interface for device management.

    Application use cases depend on this abstraction, not directly on SQLAlchemy.
    """

    @abstractmethod
    def create(self, device: DeviceMaster) -> DeviceMaster:
        pass

    @abstractmethod
    def list(self) -> List[DeviceMaster]:
        pass

    @abstractmethod
    def list_by_bed_id(self, bed_id: int) -> List[DeviceMaster]:
        pass

    @abstractmethod
    def by_id(self, id: int) -> Optional[DeviceMaster]:
        pass

    @abstractmethod
    def by_serial(self, serial: str) -> Optional[DeviceMaster]:
        pass

    @abstractmethod
    def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    def exists_by_serial(self, serial: str) -> bool:
        pass

    @abstractmethod
    def exists_by_serial_except_id(self, serial: str, id: int) -> bool:
        pass

    @abstractmethod
    def update(self, device: DeviceMaster) -> DeviceMaster:
        pass

    @abstractmethod
    def assign_bed(self, device_id: int, bed_id: int) -> Optional[DeviceMaster]:
        pass

    @abstractmethod
    def unassign_bed(self, device_id: int) -> Optional[DeviceMaster]:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
    
    @abstractmethod
    def list_by_bed_ids(
        self,
        bed_ids: List[int],
    ) -> dict[int, List[str]]:
        """
        Return monitoring devices grouped by bed id.
        """