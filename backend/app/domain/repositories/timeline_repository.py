from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.timeline_event import TimelineEvent


class TimelineRepository(ABC):
    """
    Repository contract for patient timeline events.
    """

    @abstractmethod
    def create(self, timeline_event: TimelineEvent) -> TimelineEvent:
        pass

    @abstractmethod
    def list_by_patient_id(self, patient_id: int) -> List[TimelineEvent]:
        pass

    @abstractmethod
    def get_by_id(self, timeline_event_id: int) -> Optional[TimelineEvent]:
        pass