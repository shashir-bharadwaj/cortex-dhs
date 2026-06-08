from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_service import PasswordService



class ResetUserPasswordUseCase:
    """
    Use case for resetting a user's password.
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    def execute(
        self,
        user_id: int,
        password: str,
    ):
        user = self.user_repository.by_id(user_id)

        if not user:
            raise ResourceNotFoundError(
                message="User not found.",
                meta={"user_id": user_id},
            )

        user.password_hash = PasswordService.hash_password(password)

        return self.user_repository.update(user)