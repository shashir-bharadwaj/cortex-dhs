from typing import List

from app.domain.entities.vital import Vital
from app.domain.repositories.vital_repository import VitalRepository


class ListPatientVitalsUseCase:
    """
    Use case for listing vitals for a patient.
    """

    def __init__(self, vital_repository: VitalRepository):
        self.vital_repository = vital_repository

    def execute(self, patient_id: int) -> List[Vital]:
        return self.vital_repository.list_by_patient(patient_id)