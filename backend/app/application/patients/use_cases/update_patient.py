from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository


class UpdatePatientUseCase:
    """
    Use case for updating a patient.
    """

    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def execute(self, patient_id: int, patient: Patient) -> Patient:
        existing = self.patient_repository.by_id(patient_id)

        if not existing:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        patient.id = patient_id
        return self.patient_repository.update(patient)