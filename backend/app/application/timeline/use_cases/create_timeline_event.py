from app.domain.entities.timeline_event import TimelineEvent
from app.domain.repositories.timeline_repository import TimelineRepository


class CreateTimelineEventUseCase:
    """
    Use case for creating a patient timeline event.
    """

    def __init__(self, timeline_repository: TimelineRepository):
        self.timeline_repository = timeline_repository

    def execute(
        self,
        patient_id: int,
        event: str,
        type: str,
    ) -> TimelineEvent:
        timeline_event = TimelineEvent(
            id=None,
            patient_id=patient_id,
            event=event,
            type=type,
        )

        return self.timeline_repository.create(timeline_event)