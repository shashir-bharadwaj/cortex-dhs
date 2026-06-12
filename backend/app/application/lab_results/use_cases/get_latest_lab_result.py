from typing import Optional

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.lab_result import LabResult
from app.domain.repositories.lab_result_repository import LabResultRepository
from app.domain.repositories.patient_repository import PatientRepository


class GetLatestLabResultUseCase:
    """
    Return the most recent lab result for a patient.
    """

    def __init__(
        self,
        lab_result_repository: LabResultRepository,
        patient_repository: PatientRepository,
    ):
        self.lab_result_repository = lab_result_repository
        self.patient_repository = patient_repository

    def execute(self, patient_id: int) -> Optional[LabResult]:
        patient = self.patient_repository.by_id(patient_id)
        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )
        return self.lab_result_repository.get_latest_by_patient_id(patient_id)
