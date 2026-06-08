from enum import Enum


class CaseInsensitiveEnum(str, Enum):
    """
    Base enum supporting case-insensitive input parsing.
    """

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            normalized = value.strip().lower()
            for member in cls:
                if member.value.lower() == normalized:
                    return member
        return None