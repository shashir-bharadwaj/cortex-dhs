from dataclasses import dataclass
from typing import Optional

from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)


@dataclass
class Permission:
    """
    Domain entity representing a system permission.

    Example:
    --------
    module = PATIENTS
    action = CREATE

    Produces permission key:
    PATIENTS:CREATE
    """

    module: PermissionModule

    action: PermissionAction

    description: Optional[str] = None

    id: Optional[int] = None

    @property
    def key(self) -> str:
        """
        Canonical permission identifier used by RBAC checks.
        """
        return f"{self.module.value}:{self.action.value}"