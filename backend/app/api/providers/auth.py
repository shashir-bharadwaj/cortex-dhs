from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.auth.use_cases.get_current_user import (
    GetCurrentUserUseCase,
)
from app.application.auth.use_cases.login import LoginUseCase
from app.application.auth.use_cases.logout import LogoutUseCase
from app.application.auth.use_cases.update_shift import (
    UpdateShiftUseCase,
)
from app.infrastructure.security.auth_dependencies import (
    get_current_user,
    get_jwt_service,
    require_permission,
)
from app.infrastructure.security.jwt_service import JWTService
from app.infrastructure.security.password_service import (
    PasswordService,
)


class AuthProvider:
    """
    Dependency wiring for auth-related use cases.
    """

    @staticmethod
    def login_use_case(
        user_repository=Depends(
            RepositoryProvider.get_user_repository
        ),
        jwt_service: JWTService = Depends(
            get_jwt_service
        ),
    ) -> LoginUseCase:
        return LoginUseCase(
            user_repository=user_repository,
            password_service=PasswordService(),
            jwt_service=jwt_service,
        )

    @staticmethod
    def current_user_use_case() -> GetCurrentUserUseCase:
        return GetCurrentUserUseCase()

    @staticmethod
    def authenticated_user(
        current_user=Depends(get_current_user),
    ):
        """
        Provide authenticated user
        for protected routes.
        """

        return current_user

    @staticmethod
    def permission_dependency(
        module,
        action,
    ):
        """
        Expose RBAC dependency.
        """

        return require_permission(
            module=module,
            action=action,
        )

    @staticmethod
    def update_shift_use_case(
        user_repository=Depends(
            RepositoryProvider.get_user_repository
        ),
    ) -> UpdateShiftUseCase:
        return UpdateShiftUseCase(
            user_repository=user_repository
        )

    @staticmethod
    def logout_use_case() -> LogoutUseCase:
        return LogoutUseCase()