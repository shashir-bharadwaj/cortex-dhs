from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class UpdateUserStatusUseCase:
    """
    Use case for activating/deactivating a user.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(
        self,
        user_id: int,
        is_active: bool,
    ) -> User:
        user = self.user_repository.by_id(user_id)

        if not user:
            raise ResourceNotFoundError(
                message="User not found.",
                meta={"user_id": user_id},
            )

        user.is_active = is_active

        return self.user_repository.update(user)