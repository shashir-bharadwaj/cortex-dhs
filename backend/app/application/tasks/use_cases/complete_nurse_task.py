from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.nurse_task import NurseTask
from app.domain.repositories.nurse_task_repository import NurseTaskRepository


class CompleteNurseTaskUseCase:

    def __init__(self, task_repository: NurseTaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id: int) -> NurseTask:
        task = self.task_repository.complete(task_id)
        if not task:
            raise ResourceNotFoundError(f"Task {task_id} not found")
        return task
