from app.domain.entities.role import Role
from app.domain.repositories.role_repository import RoleRepository


class ListRolesUseCase:
    """
    Use case for listing all roles.
    """

    def __init__(
        self,
        role_repository: RoleRepository,
    ):
        self.role_repository = role_repository

    def execute(self) -> list[Role]:
        """
        Return all roles.
        """
        return self.role_repository.list()