from enum import Enum


class StringEnum(str, Enum):
    """
    Base enum for string-valued enums used across the domain.
    """

    @classmethod
    def values(cls) -> list[str]:
        return [member.value for member in cls]