from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums.clinical_note import (
    ClinicalNoteType,
)


class ClinicalNoteCreateRequest(BaseModel):
    """
    Create clinical note request.
    """

    note_type: ClinicalNoteType = Field(
        alias="noteType",
    )

    note_text: str = Field(
        alias="noteText",
        min_length=1,
    )

    model_config = ConfigDict(
        populate_by_name=True,
    )


class ClinicalNoteResponse(BaseModel):
    """
    Clinical note response.
    """

    id: int

    patient_id: int = Field(
        alias="patientId",
    )

    author_id: int = Field(
        alias="authorId",
    )

    author_name: str = Field(
        alias="authorName",
    )

    note_type: ClinicalNoteType = Field(
        alias="noteType",
    )

    note_text: str = Field(
        alias="noteText",
    )

    created_at: datetime = Field(
        alias="createdAt",
    )

    updated_at: datetime = Field(
        alias="updatedAt",
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )