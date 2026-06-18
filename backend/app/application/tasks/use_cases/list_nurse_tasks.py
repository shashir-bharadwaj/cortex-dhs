from typing import List, Optional

from app.domain.entities.nurse_task import NurseTask
from app.domain.enums.task import TaskStatus
from app.domain.repositories.nurse_task_repository import NurseTaskRepository


class ListNurseTasksUseCase:

    def __init__(self, task_repository: NurseTaskRepository):
        self.task_repository = task_repository

    def execute(
        self,
        status: Optional[TaskStatus] = None,
        patient_id: Optional[int] = None,
    ) -> List[NurseTask]:
        return self.task_repository.list_all(status=status, patient_id=patient_id)
