"""
Use case for authenticating a staff user.
"""

from app.core.errors.exceptions import UnauthorizedError
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.jwt_service import JWTService
from app.infrastructure.security.password_service import PasswordService


class LoginUseCase:
    """
    Authenticate a user with email and password, then issue a token.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_service: PasswordService,
        jwt_service: JWTService,
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.jwt_service = jwt_service

    def execute(
        self,
        email: str,
        password: str,
    ) -> tuple[str, User]:
        """
        Authenticate the supplied credentials.

        Flow:
        -----
        1. Load user by email.
        2. Verify account is active.
        3. Verify password against stored password hash.
        4. Create JWT token from trusted database-backed user context.
        5. Return token + mapped domain user.
        """

        user = self.user_repository.get_by_email(email)

        if not user:
            raise UnauthorizedError("Invalid credentials")

        if not user.is_active:
            raise UnauthorizedError("User account is inactive")

        if not self.password_service.verify_password(
            password,
            user.password_hash,
        ):
            raise UnauthorizedError("Invalid credentials")

        token = self.jwt_service.create_access_token(
            subject=str(user.user_id),
            extra_claims={
                "role_id": user.role_id,
                "hospital_id": user.hospital_id,
                "unit_id": user.unit_id,
            },
        )

        return token, user