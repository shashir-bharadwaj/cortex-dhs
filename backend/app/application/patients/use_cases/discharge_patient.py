from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.patient_repository import PatientRepository


class DischargePatientUseCase:
    """
    Use case for discharging a patient.
    """

    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def execute(self, patient_id: int):
        existing = self.patient_repository.by_id(patient_id)

        if not existing:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        return self.patient_repository.discharge(patient_id)