from fastapi import Depends

from app.api.providers.repositories import (
    RepositoryProvider,
)

from app.application.clinical_note.use_cases.create_clinical_note import (
    CreateClinicalNoteUseCase,
)
from app.application.clinical_note.use_cases.list_clinical_notes import (
    ListClinicalNotesUseCase,
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


class ClinicalNoteProvider:
    """
    Provider for Clinical Note use cases.
    """

    @staticmethod
    def get_create_clinical_note_use_case(
        clinical_note_repository: ClinicalNoteRepository = Depends(
            RepositoryProvider.get_clinical_note_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
        user_repository: UserRepository = Depends(
            RepositoryProvider.get_user_repository
        ),
    ) -> CreateClinicalNoteUseCase:
        """
        Build create clinical note use case.
        """

        return CreateClinicalNoteUseCase(
            clinical_note_repository=clinical_note_repository,
            patient_repository=patient_repository,
            user_repository=user_repository,
        )

    @staticmethod
    def get_list_clinical_notes_use_case(
        clinical_note_repository: ClinicalNoteRepository = Depends(
            RepositoryProvider.get_clinical_note_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> ListClinicalNotesUseCase:
        """
        Build list clinical notes use case.
        """

        return ListClinicalNotesUseCase(
            clinical_note_repository=clinical_note_repository,
            patient_repository=patient_repository,
        )