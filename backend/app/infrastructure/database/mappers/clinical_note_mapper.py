from typing import List

from app.domain.entities.clinical_note import (
    ClinicalNote,
)
from app.infrastructure.database.models.clinical_note import (
    ClinicalNoteModel,
)


class ClinicalNoteMapper:
    """
    Mapper responsible for converting ClinicalNote
    domain entities and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: ClinicalNoteModel,
    ) -> ClinicalNote:
        """
        Convert SQLAlchemy model -> domain entity.
        """

        return ClinicalNote(
            id=model.id,
            patient_id=model.patient_id,
            author_id=model.author_id,
            author_name=model.author_name,
            note_type=model.note_type,
            note_text=model.note_text,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(
        entity: ClinicalNote,
    ) -> ClinicalNoteModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """

        return ClinicalNoteModel(
            id=entity.id,
            patient_id=entity.patient_id,
            author_id=entity.author_id,
            author_name=entity.author_name,
            note_type=entity.note_type,
            note_text=entity.note_text,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain_list(
        models: List[ClinicalNoteModel],
    ) -> List[ClinicalNote]:
        """
        Convert model list -> domain entity list.
        """

        return [
            ClinicalNoteMapper.to_domain(model)
            for model in models
        ]