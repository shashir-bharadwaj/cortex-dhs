from typing import List

from app.domain.entities.timeline_event import TimelineEvent
from app.infrastructure.database.models.timeline import (
    TimelineEventModel,
)


class TimelineEventMapper:
    """
    Mapper responsible for converting TimelineEvent domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: TimelineEventModel,
    ) -> TimelineEvent:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        return TimelineEvent(
            id=model.id,
            patient_id=model.patient_id,
            event=model.event,
            type=model.type,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(
        entity: TimelineEvent,
    ) -> TimelineEventModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return TimelineEventModel(
            id=entity.id,
            patient_id=entity.patient_id,
            event=entity.event,
            type=entity.type,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_domain_list(
        models: List[TimelineEventModel],
    ) -> List[TimelineEvent]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            TimelineEventMapper.to_domain(model)
            for model in models
        ]