from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository


class GetPatientUseCase:
    """
    Use case for reading a single patient.
    """

    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def execute(self, patient_id: int) -> Patient:
        patient = self.patient_repository.by_id(patient_id)

        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        return patient