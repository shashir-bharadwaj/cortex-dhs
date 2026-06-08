from abc import ABC, abstractmethod

from app.domain.entities.hospital import Hospital, HospitalUnit


class HospitalRepository(ABC):
    """
    Domain repository interface for hospital management.

    Use cases depend on this interface, not on SQLAlchemy implementations.
    """

    @abstractmethod
    def create_hospital(self, hospital: Hospital) -> Hospital:
        raise NotImplementedError

    @abstractmethod
    def get_hospital(self, hospital_id: int) -> Hospital | None:
        raise NotImplementedError

    @abstractmethod
    def list_hospitals(self) -> list[Hospital]:
        raise NotImplementedError

    @abstractmethod
    def create_unit(self, unit: HospitalUnit) -> HospitalUnit:
        raise NotImplementedError

    @abstractmethod
    def get_unit(self, unit_id: int) -> HospitalUnit | None:
        raise NotImplementedError

    @abstractmethod
    def list_units(self, hospital_id: int | None = None) -> list[HospitalUnit]:
        raise NotImplementedError