from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.role import Role


class RoleRepository(ABC):
    """
    Repository contract for role persistence operations.
    """

    @abstractmethod
    def create(self, role: Role) -> Role:
        """
        Persist a new role.
        """
        raise NotImplementedError

    @abstractmethod
    def by_id(self, role_id: int) -> Optional[Role]:
        """
        Retrieve role by id.
        """
        raise NotImplementedError

    @abstractmethod
    def by_name(self, name: str) -> Optional[Role]:
        """
        Retrieve role by name.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Role]:
        """
        List all roles.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, role: Role) -> Role:
        """
        Update an existing role.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, role_id: int) -> None:
        """
        Delete a role.
        """
        raise NotImplementedError