from dataclasses import dataclass
from typing import Optional

from app.domain.enums.auth import ShiftType


@dataclass
class User:
    """
    Domain entity representing a platform user.

    Business role:
    --------------
    Represents an authenticated system user who belongs to a hospital
    and optionally to a hospital unit.

    RBAC note:
    ----------
    role_id is the source of truth for permission checks.
    role is kept as an optional display/enrichment field.
    """

    user_id: str

    first_name: str
    last_name: str
    email: str

    password_hash: str

    role_id: int

    hospital_id: Optional[int] = None
    unit_id: Optional[int] = None

    shift: Optional[ShiftType] = None

    is_active: bool = True

    id: Optional[int] = None
    role: Optional[str] = None

    @property
    def name(self) -> str:
        """
        Full display name used by auth response contracts.
        """
        return f"{self.first_name} {self.last_name}".strip()