from app.core.errors.exceptions import ConflictError
from app.domain.entities.user import User
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_service import PasswordService


class CreateUserUseCase:
    """
    Use case for creating platform users.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def execute(self, user: User, password: str) -> User:
        """
        Create a new user with hashed password.
        """

        existing_user = self.user_repository.get_by_user_id(
            user.user_id
        )

        if existing_user:
            raise ConflictError(
                message="User ID already exists.",
            )

        existing_email = self.user_repository.get_by_email(
            user.email
        )

        if existing_email:
            raise ConflictError(
                message="Email already exists.",
            )

        role = self.role_repository.by_id(user.role_id)

        if not role:
            raise ConflictError(
                message="Invalid role selected.",
            )

        user.password_hash = PasswordService().hash_password(password)

        return self.user_repository.create(user)