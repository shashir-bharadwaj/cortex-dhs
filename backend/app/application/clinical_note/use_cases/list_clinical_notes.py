from app.core.errors.exceptions import (
    ResourceNotFoundError,
)
from app.domain.repositories.clinical_note_repository import (
    ClinicalNoteRepository,
)
from app.domain.repositories.patient_repository import (
    PatientRepository,
)


class ListClinicalNotesUseCase:
    """
    Return clinical notes for a patient.
    """

    def __init__(
        self,
        clinical_note_repository: ClinicalNoteRepository,
        patient_repository: PatientRepository,
    ):
        self.clinical_note_repository = (
            clinical_note_repository
        )
        self.patient_repository = (
            patient_repository
        )

    def execute(
        self,
        patient_id: int,
    ):
        """
        Return all notes for a patient.
        """

        patient = self.patient_repository.by_id(
            patient_id
        )

        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={
                    "patient_id": patient_id,
                },
            )

        return (
            self.clinical_note_repository
            .list_by_patient_id(patient_id)
        )