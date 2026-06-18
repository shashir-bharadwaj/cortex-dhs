from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.nurse_task import NurseTask
from app.domain.enums.task import TaskStatus


class NurseTaskRepository(ABC):

    @abstractmethod
    def create(self, task: NurseTask) -> NurseTask:
        pass

    @abstractmethod
    def list_all(
        self,
        status: Optional[TaskStatus] = None,
        patient_id: Optional[int] = None,
    ) -> List[NurseTask]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[NurseTask]:
        pass

    @abstractmethod
    def complete(self, task_id: int) -> Optional[NurseTask]:
        pass

    @abstractmethod
    def count_pending_by_patient(self, patient_id: int) -> int:
        pass
