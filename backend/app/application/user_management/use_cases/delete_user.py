from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.user_repository import UserRepository


class DeleteUserUseCase:
    """
    Use case for soft deleting a user.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> None:
        user = self.user_repository.by_id(user_id)

        if not user:
            raise ResourceNotFoundError(
                message="User not found.",
                meta={"user_id": user_id},
            )

        self.user_repository.delete(user_id)