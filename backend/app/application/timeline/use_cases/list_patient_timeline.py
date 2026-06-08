from typing import List

from app.domain.entities.timeline_event import TimelineEvent
from app.domain.repositories.timeline_repository import TimelineRepository


class ListPatientTimelineUseCase:
    """
    Use case for listing timeline events for a patient.
    """

    def __init__(self, timeline_repository: TimelineRepository):
        self.timeline_repository = timeline_repository

    def execute(self, patient_id: int) -> List[TimelineEvent]:
        return self.timeline_repository.list_by_patient_id(patient_id)