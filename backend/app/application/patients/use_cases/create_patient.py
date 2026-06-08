from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository


class CreatePatientUseCase:
    """
    Use case for creating a patient.
    """

    def __init__(
        self,
        patient_repository: PatientRepository,
    ):
        self.patient_repository = patient_repository

    def execute(
        self,
        patient: Patient,
    ) -> Patient:
        """
        Persist a new patient admission.
        """

        return self.patient_repository.create(patient)