from dataclasses import dataclass
from typing import Optional


@dataclass
class Role:
    """
    Domain entity representing a user role.

    Business role:
    --------------
    Defines a named access group such as Admin, Doctor, or Nurse.

    RBAC note:
    ----------
    Permissions should be attached through RolePermission mappings,
    not stored directly inside this entity.
    """

    name: str
    description: Optional[str] = None

    id: Optional[int] = None