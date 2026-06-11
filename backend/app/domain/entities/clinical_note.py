from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.enums.clinical_note import ClinicalNoteType


@dataclass
class ClinicalNote:
    """
    Domain entity representing a clinical note for a patient.
    """

    id: Optional[int] = None

    patient_id: Optional[int] = None

    author_id: Optional[int] = None
    author_name: Optional[str] = None

    note_type: ClinicalNoteType = ClinicalNoteType.PROGRESS
    note_text: str = ""

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None