from enum import Enum


class ClinicalNoteType(str, Enum):
    """
    Supported clinical note categories.
    """

    PROGRESS = "progress"
    NURSING = "nursing"
    ORDER = "order"
    HANDOVER = "handover"