from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.permission import Permission
from app.domain.enums.permission import PermissionAction, PermissionModule


class PermissionRepository(ABC):
    """
    Repository contract for permission persistence operations.
    """

    @abstractmethod
    def create(self, permission: Permission) -> Permission:
        """
        Persist a new permission.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, permission_id: int) -> Optional[Permission]:
        """
        Retrieve permission by id.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_module_action(
        self,
        module: PermissionModule,
        action: PermissionAction,
    ) -> Optional[Permission]:
        """
        Retrieve permission by module and action.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Permission]:
        """
        List all permissions.
        """
        raise NotImplementedError