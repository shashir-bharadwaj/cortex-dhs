from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthenticatedUser:
    """
    Runtime authenticated user context.

    This entity is used specifically for authentication and RBAC checks.

    Unlike the normal User entity, this includes resolved permissions
    so authorization checks do not need additional database lookups.
    """

    id: int
    user_id: str
    email: str

    role_id: int
    role_name: str

    hospital_id: Optional[int]
    unit_id: Optional[int]

    is_active: bool

    permissions: set[str]

    def has_permission(self, permission_key: str) -> bool:
        """
        Check whether user has a specific permission.

        Expected format:
            MODULE:ACTION

        Example:
            MANAGE_USERS:VIEW
        """
        return permission_key in self.permissions