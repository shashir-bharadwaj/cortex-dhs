from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.timeline_event import TimelineEvent
from app.domain.repositories.timeline_repository import (
    TimelineRepository,
)
from app.infrastructure.database.mappers.timeline_event_mapper import (
    TimelineEventMapper,
)
from app.infrastructure.database.models.timeline import (
    TimelineEventModel,
)


class SQLAlchemyTimelineRepository(TimelineRepository):
    """
    SQLAlchemy implementation of TimelineRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        timeline_event: TimelineEvent,
    ) -> TimelineEvent:
        model = TimelineEventMapper.to_model(
            timeline_event
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return TimelineEventMapper.to_domain(model)

    def list_by_patient_id(
        self,
        patient_id: int,
    ) -> List[TimelineEvent]:
        models = (
            self.db.query(TimelineEventModel)
            .filter(
                TimelineEventModel.patient_id == patient_id
            )
            .order_by(
                TimelineEventModel.created_at.desc()
            )
            .all()
        )

        return TimelineEventMapper.to_domain_list(
            models
        )

    def get_by_id(
        self,
        timeline_event_id: int,
    ) -> Optional[TimelineEvent]:
        model = (
            self.db.query(TimelineEventModel)
            .filter(
                TimelineEventModel.id == timeline_event_id
            )
            .first()
        )

        if not model:
            return None

        return TimelineEventMapper.to_domain(model)