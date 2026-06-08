from abc import ABC, abstractmethod

from app.domain.entities.role_permission import RolePermission


class RolePermissionRepository(ABC):
    """
    Repository contract for role-permission assignment operations.
    """

    @abstractmethod
    def assign_permission(
        self,
        role_permission: RolePermission,
    ) -> RolePermission:
        raise NotImplementedError

    @abstractmethod
    def remove_permission(
        self,
        role_id: int,
        permission_id: int,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_by_role(self, role_id: int) -> list[RolePermission]:
        raise NotImplementedError

    @abstractmethod
    def permissions_by_role(
        self,
        role_id: int,
    ) -> dict[str, list[str]]:
        """
        Return assigned permissions grouped by module.

        Example:
        {
            "PATIENTS": ["VIEW", "CREATE"],
            "VITALS": ["VIEW"]
        }
        """
        raise NotImplementedError

    @abstractmethod
    def role_has_permission(
        self,
        role_id: int,
        permission_key: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def replace_permissions(
        self,
        role_id: int,
        permission_ids: list[int],
    ) -> None:
        raise NotImplementedError