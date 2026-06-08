from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository


class ChangeUserRoleUseCase:
    """
    Use case for changing a user's role.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def execute(
        self,
        user_id: int,
        role_id: int,
    ):
        user = self.user_repository.by_id(user_id)

        if not user:
            raise ResourceNotFoundError(
                message="User not found.",
                meta={"user_id": user_id},
            )

        role = self.role_repository.by_id(role_id)

        if not role:
            raise ResourceNotFoundError(
                message="Role not found.",
                meta={"role_id": role_id},
            )

        user.role_id = role_id

        return self.user_repository.update(user)