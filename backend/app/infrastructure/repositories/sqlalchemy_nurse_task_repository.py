from datetime import UTC, datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.nurse_task import NurseTask
from app.domain.enums.task import TaskStatus
from app.domain.repositories.nurse_task_repository import NurseTaskRepository
from app.infrastructure.database.mappers.nurse_task_mapper import NurseTaskMapper
from app.infrastructure.database.models.nurse_task import NurseTaskModel


class SQLAlchemyNurseTaskRepository(NurseTaskRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, task: NurseTask) -> NurseTask:
        model = NurseTaskMapper.to_model(task)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return NurseTaskMapper.to_domain(model)

    def list_all(
        self,
        status: Optional[TaskStatus] = None,
        patient_id: Optional[int] = None,
    ) -> List[NurseTask]:
        query = self.db.query(NurseTaskModel)
        if status is not None:
            query = query.filter(NurseTaskModel.status == status.value)
        if patient_id is not None:
            query = query.filter(NurseTaskModel.patient_id == patient_id)
        models = query.order_by(NurseTaskModel.due_time.asc()).all()
        return NurseTaskMapper.to_domain_list(models)

    def get_by_id(self, task_id: int) -> Optional[NurseTask]:
        model = self.db.query(NurseTaskModel).filter(NurseTaskModel.id == task_id).first()
        return NurseTaskMapper.to_domain(model) if model else None

    def complete(self, task_id: int) -> Optional[NurseTask]:
        model = self.db.query(NurseTaskModel).filter(NurseTaskModel.id == task_id).first()
        if not model:
            return None
        model.status = TaskStatus.COMPLETED
        model.completed_at = datetime.now(UTC)
        self.db.commit()
        self.db.refresh(model)
        return NurseTaskMapper.to_domain(model)

    def count_pending_by_patient(self, patient_id: int) -> int:
        return (
            self.db.query(NurseTaskModel)
            .filter(
                NurseTaskModel.patient_id == patient_id,
                NurseTaskModel.status == TaskStatus.PENDING.value,
            )
            .count()
        )
