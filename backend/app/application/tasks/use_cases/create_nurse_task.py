from datetime import datetime
from typing import Optional

from app.core.errors.exceptions import PatientNotFoundError, ResourceNotFoundError
from app.domain.entities.nurse_task import NurseTask
from app.domain.enums.task import TaskStatus
from app.domain.repositories.nurse_task_repository import NurseTaskRepository
from app.domain.repositories.patient_repository import PatientRepository


class CreateNurseTaskUseCase:

    def __init__(
        self,
        task_repository: NurseTaskRepository,
        patient_repository: PatientRepository,
    ):
        self.task_repository = task_repository
        self.patient_repository = patient_repository

    def execute(
        self,
        patient_id: int,
        title: str,
        description: Optional[str] = None,
        due_time: Optional[datetime] = None,
        assigned_to_id: Optional[int] = None,
    ) -> NurseTask:
        patient = self.patient_repository.get_by_id(patient_id)
        if not patient:
            raise PatientNotFoundError(patient_id)

        bed_label = ""
        if patient.bed:
            bed_label = patient.bed.bed_id
        elif patient.bed_id:
            bed_label = str(patient.bed_id)

        task = NurseTask(
            patient_id=patient_id,
            patient_name=patient.name,
            bed_label=bed_label,
            assigned_to_id=assigned_to_id,
            title=title,
            description=description,
            due_time=due_time,
            status=TaskStatus.PENDING,
        )
        return self.task_repository.create(task)
