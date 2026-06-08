from dataclasses import dataclass
from typing import Optional


@dataclass
class RolePermission:
    """
    Domain entity representing role-permission mapping.
    """

    role_id: int

    permission_id: int

    id: Optional[int] = None