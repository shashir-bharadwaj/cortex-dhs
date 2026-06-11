from typing import List

from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.providers.clinical_note import ClinicalNoteProvider
from app.api.schemas.clinical_note import (
    ClinicalNoteCreateRequest,
    ClinicalNoteResponse,
)
from app.application.clinical_note.use_cases.create_clinical_note import (
    CreateClinicalNoteUseCase,
)
from app.application.clinical_note.use_cases.list_clinical_notes import (
    ListClinicalNotesUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)

router = APIRouter(
    prefix="/patients",
    tags=["Clinical Notes"],
)


def patient_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for reading patient notes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.PATIENTS,
            action,
        )
    )


def timeline_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for writing patient documentation.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.TIMELINE,
            action,
        )
    )


@router.post(
    "/{patient_id}/notes",
    response_model=ClinicalNoteResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_clinical_note(
    patient_id: int,
    payload: ClinicalNoteCreateRequest,
    current_user=timeline_permission(
        PermissionAction.CREATE
    ),
    use_case: CreateClinicalNoteUseCase = Depends(
        ClinicalNoteProvider.get_create_clinical_note_use_case
    ),
) -> ClinicalNoteResponse:
    """
    Create a clinical note for a patient.

    Author information is derived from the authenticated user.
    """

    note = use_case.execute(
        patient_id=patient_id,
        author_id=current_user.id,
        note_type=payload.note_type,
        note_text=payload.note_text,
    )

    return ClinicalNoteResponse.model_validate(note)


@router.get(
    "/{patient_id}/notes",
    response_model=List[ClinicalNoteResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_clinical_notes(
    patient_id: int,
    current_user=patient_permission(
        PermissionAction.VIEW
    ),
    use_case: ListClinicalNotesUseCase = Depends(
        ClinicalNoteProvider.get_list_clinical_notes_use_case
    ),
) -> List[ClinicalNoteResponse]:
    """
    Return clinical notes for a patient.
    """

    notes = use_case.execute(
        patient_id=patient_id,
    )

    return [
        ClinicalNoteResponse.model_validate(note)
        for note in notes
    ]