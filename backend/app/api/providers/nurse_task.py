from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.tasks.use_cases.create_nurse_task import CreateNurseTaskUseCase
from app.application.tasks.use_cases.list_nurse_tasks import ListNurseTasksUseCase
from app.application.tasks.use_cases.complete_nurse_task import CompleteNurseTaskUseCase
from app.infrastructure.repositories.sqlalchemy_nurse_task_repository import (
    SQLAlchemyNurseTaskRepository,
)
from app.infrastructure.repositories.sqlalchemy_patient_repository import (
    SQLAlchemyPatientRepository,
)


class NurseTaskProvider:

    @staticmethod
    def get_create_use_case(
        task_repository: SQLAlchemyNurseTaskRepository = Depends(
            RepositoryProvider.get_nurse_task_repository
        ),
        patient_repository: SQLAlchemyPatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> CreateNurseTaskUseCase:
        return CreateNurseTaskUseCase(
            task_repository=task_repository,
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_list_use_case(
        task_repository: SQLAlchemyNurseTaskRepository = Depends(
            RepositoryProvider.get_nurse_task_repository
        ),
    ) -> ListNurseTasksUseCase:
        return ListNurseTasksUseCase(task_repository=task_repository)

    @staticmethod
    def get_complete_use_case(
        task_repository: SQLAlchemyNurseTaskRepository = Depends(
            RepositoryProvider.get_nurse_task_repository
        ),
    ) -> CompleteNurseTaskUseCase:
        return CompleteNurseTaskUseCase(task_repository=task_repository)
