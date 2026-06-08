from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class ListUsersUseCase:
    """
    Use case for listing users.
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    def execute(self) -> list[User]:
        """
        Return all users.
        """
        return self.user_repository.list()