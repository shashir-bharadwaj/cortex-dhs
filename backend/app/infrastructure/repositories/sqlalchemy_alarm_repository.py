from typing import List

from sqlalchemy.orm import Session

from app.domain.entities.alarm import Alarm
from app.domain.repositories.alarm_repository import AlarmRepository
from app.infrastructure.database.models.alarm import AlarmModel
from app.infrastructure.database.mappers.alarm_mapper import AlarmMapper


class SQLAlchemyAlarmRepository(AlarmRepository):
    """
    SQLAlchemy implementation of AlarmRepository.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, alarm: Alarm) -> Alarm:
        model = AlarmMapper.to_model(alarm)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return AlarmMapper.to_domain(model)

    def list(
        self,
        hospital_id: str | None = None,
        unit_id: str | None = None,
        severity: str | None = None,
        acknowledged: bool | None = None,
        silenced: bool | None = None,
        patient_id: int | None = None,
    ) -> List[Alarm]:

        query = self.db.query(AlarmModel)

        # NOTE: hospital_id and unit_id are not directly in AlarmModel,
        # so we skip them for now unless we join Patient later.

        if severity:
            query = query.filter(AlarmModel.severity == severity)

        if acknowledged is not None:
            query = query.filter(AlarmModel.acknowledged == acknowledged)

        if silenced is not None:
            query = query.filter(AlarmModel.silenced == silenced)

        if patient_id:
            query = query.filter(AlarmModel.patient_id == patient_id)

        models = query.order_by(AlarmModel.timestamp.desc()).all()

        return [AlarmMapper.to_domain(m) for m in models]

    def by_id(self, alarm_id: int) -> Alarm | None:
        model = (
            self.db.query(AlarmModel)
            .filter(AlarmModel.id == alarm_id)
            .first()
        )

        if not model:
            return None

        return AlarmMapper.to_domain(model)

    def by_patient(
        self,
        patient_id: int,
        acknowledged: bool | None = None,
    ) -> List[Alarm]:

        query = self.db.query(AlarmModel).filter(
            AlarmModel.patient_id == patient_id
        )

        if acknowledged is not None:
            query = query.filter(AlarmModel.acknowledged == acknowledged)

        models = query.order_by(AlarmModel.timestamp.desc()).all()

        return [AlarmMapper.to_domain(m) for m in models]

    def save(self, alarm: Alarm) -> Alarm:
        model = (
            self.db.query(AlarmModel)
            .filter(AlarmModel.id == alarm.id)
            .first()
        )

        if not model:
            raise ValueError("Alarm not found")

        model = AlarmMapper.apply_to_model(alarm, model)

        self.db.commit()
        self.db.refresh(model)

        return AlarmMapper.to_domain(model)
    
    def list_active_by_patient_ids(
        self,
        patient_ids: List[int],
    ) -> List[Alarm]:
        """
        Return active/unacknowledged alarms for dashboard patient cards.

        Current business rule:
        - an alarm is considered active if it is not acknowledged
        """

        if not patient_ids:
            return []

        models = (
            self.db.query(AlarmModel)
            .filter(
                AlarmModel.patient_id.in_(patient_ids),
                AlarmModel.acknowledged.is_(False),
                AlarmModel.silenced.is_(False),
            )
            .order_by(AlarmModel.timestamp.desc())
            .all()
        )

        return [AlarmMapper.to_domain(model) for model in models]

    def list_recent_by_patient_ids(
        self,
        patient_ids: List[int],
        limit: int = 50,
    ) -> List[Alarm]:
        """
        Return recent alarms for dashboard alarm list.
        """

        if not patient_ids:
            return []

        models = (
            self.db.query(AlarmModel)
            .filter(AlarmModel.patient_id.in_(patient_ids))
            .order_by(AlarmModel.timestamp.desc())
            .limit(limit)
            .all()
        )

        return [AlarmMapper.to_domain(model) for model in models]
    
    def create_from_ingestion(
        self,
        data: dict,
    ):
        """
        Persist ingestion-generated Alarm row.
        """
        model = AlarmModel(
            timestamp=data["timestamp"],
            patient_id=data["patient_id"],
            patient_name=data["patient_name"],
            bed_id=data["bed_id"],
            device=data["device"],
            message=data["message"],
            severity=data["severity"],
            acknowledged=data["acknowledged"],
            silenced=data["silenced"],
            escalated=data["escalated"],
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return AlarmMapper.to_domain(model)