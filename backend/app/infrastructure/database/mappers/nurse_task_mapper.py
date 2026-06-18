from typing import List

from app.domain.entities.nurse_task import NurseTask
from app.infrastructure.database.models.nurse_task import NurseTaskModel


class NurseTaskMapper:

    @staticmethod
    def to_domain(model: NurseTaskModel) -> NurseTask:
        return NurseTask(
            id=model.id,
            patient_id=model.patient_id,
            patient_name=model.patient_name,
            bed_label=model.bed_label,
            assigned_to_id=model.assigned_to_id,
            title=model.title,
            description=model.description,
            due_time=model.due_time,
            status=model.status,
            created_at=model.created_at,
            completed_at=model.completed_at,
        )

    @staticmethod
    def to_model(entity: NurseTask) -> NurseTaskModel:
        return NurseTaskModel(
            id=entity.id,
            patient_id=entity.patient_id,
            patient_name=entity.patient_name,
            bed_label=entity.bed_label,
            assigned_to_id=entity.assigned_to_id,
            title=entity.title,
            description=entity.description,
            due_time=entity.due_time,
            status=entity.status,
            created_at=entity.created_at,
            completed_at=entity.completed_at,
        )

    @staticmethod
    def to_domain_list(models: List[NurseTaskModel]) -> List[NurseTask]:
        return [NurseTaskMapper.to_domain(m) for m in models]
