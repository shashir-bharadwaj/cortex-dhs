from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.clinical_note import (
    ClinicalNote,
)
from app.domain.repositories.clinical_note_repository import (
    ClinicalNoteRepository,
)
from app.infrastructure.database.mappers.clinical_note_mapper import (
    ClinicalNoteMapper,
)
from app.infrastructure.database.models.clinical_note import (
    ClinicalNoteModel,
)


class SQLAlchemyClinicalNoteRepository(
    ClinicalNoteRepository
):
    """
    SQLAlchemy implementation of ClinicalNoteRepository.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        note: ClinicalNote,
    ) -> ClinicalNote:
        """
        Persist a new clinical note.
        """

        model = ClinicalNoteMapper.to_model(
            note
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return ClinicalNoteMapper.to_domain(
            model
        )

    def list_by_patient_id(
        self,
        patient_id: int,
    ) -> List[ClinicalNote]:
        """
        Return all notes for a patient.
        """

        models = (
            self.db.query(
                ClinicalNoteModel
            )
            .filter(
                ClinicalNoteModel.patient_id
                == patient_id
            )
            .order_by(
                ClinicalNoteModel.created_at.desc()
            )
            .all()
        )

        return (
            ClinicalNoteMapper.to_domain_list(
                models
            )
        )

    def by_id(
        self,
        note_id: int,
    ) -> Optional[ClinicalNote]:
        """
        Return note by id.
        """

        model = (
            self.db.query(
                ClinicalNoteModel
            )
            .filter(
                ClinicalNoteModel.id
                == note_id
            )
            .first()
        )

        if not model:
            return None

        return ClinicalNoteMapper.to_domain(
            model
        )

    def delete(
        self,
        note_id: int,
    ) -> None:
        """
        Delete a clinical note.
        """

        model = (
            self.db.query(
                ClinicalNoteModel
            )
            .filter(
                ClinicalNoteModel.id
                == note_id
            )
            .first()
        )

        if model:
            self.db.delete(model)
            self.db.commit()