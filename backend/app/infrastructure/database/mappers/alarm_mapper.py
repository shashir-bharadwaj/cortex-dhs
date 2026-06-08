from typing import List

from app.domain.entities.alarm import Alarm
from app.domain.enums.alarm import AlarmSeverity
from app.infrastructure.database.models.alarm import AlarmModel


class AlarmMapper:
    """
    Mapper responsible for converting Alarm domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(model: AlarmModel) -> Alarm:
        return Alarm(
            id=model.id,
            timestamp=model.timestamp,
            patient_id=model.patient_id,
            patient_name=model.patient_name,
            bed_id=model.bed_id,
            device=model.device,
            message=model.message,
            severity=AlarmSeverity(model.severity),
            acknowledged=model.acknowledged,
            silenced=model.silenced,
            escalated=model.escalated,
            acknowledged_by=model.acknowledged_by,
            silenced_by=model.silenced_by,
            silence_until=model.silence_until,
            escalated_by=model.escalated_by,
            escalate_to=model.escalate_to,
        )

    @staticmethod
    def to_model(entity: Alarm) -> AlarmModel:
        return AlarmModel(
            id=entity.id,
            timestamp=entity.timestamp,
            patient_id=entity.patient_id,
            patient_name=entity.patient_name,
            bed_id=entity.bed_id,
            device=entity.device,
            message=entity.message,
            severity=entity.severity.value,
            acknowledged=entity.acknowledged,
            silenced=entity.silenced,
            escalated=entity.escalated,
            acknowledged_by=entity.acknowledged_by,
            silenced_by=entity.silenced_by,
            silence_until=entity.silence_until,
            escalated_by=entity.escalated_by,
            escalate_to=entity.escalate_to,
        )

    @staticmethod
    def apply_to_model(
        entity: Alarm,
        model: AlarmModel,
    ) -> AlarmModel:
        model.timestamp = entity.timestamp
        model.patient_id = entity.patient_id
        model.patient_name = entity.patient_name
        model.bed_id = entity.bed_id
        model.device = entity.device
        model.message = entity.message
        model.severity = entity.severity.value
        model.acknowledged = entity.acknowledged
        model.silenced = entity.silenced
        model.escalated = entity.escalated
        model.acknowledged_by = entity.acknowledged_by
        model.silenced_by = entity.silenced_by
        model.silence_until = entity.silence_until
        model.escalated_by = entity.escalated_by
        model.escalate_to = entity.escalate_to

        return model

    @staticmethod
    def to_domain_list(
        models: List[AlarmModel],
    ) -> List[Alarm]:
        return [
            AlarmMapper.to_domain(model)
            for model in models
        ]