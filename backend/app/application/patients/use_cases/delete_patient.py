from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.patient_repository import PatientRepository


class DeletePatientUseCase:
    """
    Use case for permanently deleting a patient and dependent records.
    """

    def __init__(
        self,
        patient_repository: PatientRepository,
    ):
        self.patient_repository = patient_repository

    def execute(self, patient_id: int) -> None:
        deleted = self.patient_repository.delete(patient_id)

        if not deleted:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )
