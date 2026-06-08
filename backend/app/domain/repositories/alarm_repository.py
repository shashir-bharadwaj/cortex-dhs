from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.alarm import Alarm


class AlarmRepository(ABC):
    """
    Repository contract for alarm persistence.

    Application use cases depend on this abstraction, not SQLAlchemy.
    """

    @abstractmethod
    def create(self, alarm: Alarm) -> Alarm:
        """
        Persist a new alarm.
        """

    @abstractmethod
    def list(
        self,
        hospital_id: str | None = None,
        unit_id: str | None = None,
        severity: str | None = None,
        acknowledged: bool | None = None,
        silenced: bool | None = None,
        patient_id: int | None = None,
    ) -> List[Alarm]:
        """
        Return alarms with optional filters.
        """

    @abstractmethod
    def by_id(self, alarm_id: int) -> Alarm | None:
        """
        Return alarm by id.
        """

    @abstractmethod
    def by_patient(
        self,
        patient_id: int,
        acknowledged: bool | None = None,
    ) -> List[Alarm]:
        """
        Return alarms for a patient.
        """

    @abstractmethod
    def save(self, alarm: Alarm) -> Alarm:
        """
        Persist changes to an existing alarm.
        """

    @abstractmethod
    def list_recent_by_patient_ids(
        self,
        patient_ids: List[int],
        limit: int = 50,
    ) -> List[Alarm]:
        """
        Fetch recent alarms for dashboard display.
        """

    @abstractmethod
    def list_active_by_patient_ids(
        self,
        patient_ids: List[int],
    ) -> List[Alarm]:
        """
        Fetch active alarms for dashboard aggregation.
        """

    @abstractmethod
    def create_from_ingestion(
        self,
        data: dict,
    ):
        pass