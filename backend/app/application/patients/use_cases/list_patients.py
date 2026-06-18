from typing import List

from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository


class ListPatientsUseCase:
    """
    Use case for listing patients.
    """

    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def execute(
        self,
        limit: int | None = None,
        offset: int = 0,
    ) -> List[Patient]:
        return self.patient_repository.list(limit=limit, offset=offset)

    def count(self) -> int:
        return self.patient_repository.count()