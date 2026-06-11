from app.core.errors.exceptions import (
    ResourceNotFoundError,
)
from app.domain.entities.clinical_note import (
    ClinicalNote,
)
from app.domain.enums.clinical_note import (
    ClinicalNoteType,
)
from app.domain.repositories.clinical_note_repository import (
    ClinicalNoteRepository,
)
from app.domain.repositories.patient_repository import (
    PatientRepository,
)
from app.domain.repositories.user_repository import (
    UserRepository,
)


class CreateClinicalNoteUseCase:
    """
    Create a clinical note for a patient.
    """

    def __init__(
        self,
        clinical_note_repository: ClinicalNoteRepository,
        patient_repository: PatientRepository,
        user_repository: UserRepository,
    ):
        self.clinical_note_repository = clinical_note_repository
        self.patient_repository = patient_repository
        self.user_repository = user_repository

    def execute(
        self,
        patient_id: int,
        author_id: int,
        note_type: ClinicalNoteType,
        note_text: str,
    ) -> ClinicalNote:
        """
        Create a new clinical note.
        """

        patient = self.patient_repository.by_id(patient_id)

        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        user = self.user_repository.by_id(author_id)

        if not user:
            raise ResourceNotFoundError(
                message="User not found.",
                meta={"user_id": author_id},
            )

        note = ClinicalNote(
            patient_id=patient_id,
            author_id=user.id,
            author_name=user.name,
            note_type=note_type,
            note_text=note_text,
        )

        return self.clinical_note_repository.create(note)