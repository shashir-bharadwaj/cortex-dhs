from collections.abc import Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from app.api.providers.repositories import RepositoryProvider
from app.core.errors.exceptions import (
    ForbiddenError,
    UnauthorizedError,
)
from app.domain.entities.authenticated_user import (
    AuthenticatedUser,
)
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)
from app.infrastructure.security.jwt_service import JWTService

security = HTTPBearer()


def get_jwt_service() -> JWTService:
    """
    Provide JWT service instance.
    """
    return JWTService()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service),
    user_repository=Depends(
        RepositoryProvider.get_user_repository
    ),
) -> AuthenticatedUser:
    """
    Resolve authenticated user from JWT token.

    Loads full RBAC context including permissions.
    """

    token = credentials.credentials

    payload = jwt_service.decode_token(token)

    if not payload:
        raise UnauthorizedError(
            message="Invalid authentication token.",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise UnauthorizedError(
            message="Invalid authentication token payload.",
        )

    user = user_repository.get_auth_context_by_user_id(
        user_id
    )

    if not user:
        raise UnauthorizedError(
            message="User not found.",
        )

    if not user.is_active:
        raise UnauthorizedError(
            message="User account is inactive.",
        )

    return user


def build_permission_key(
    module: PermissionModule,
    action: PermissionAction,
) -> str:
    """
    Build normalized RBAC permission key.
    """

    return f"{module.value}:{action.value}"


def require_permission(
    module: PermissionModule,
    action: PermissionAction,
) -> Callable:
    """
    Route-level RBAC permission dependency.
    """

    def dependency(
        current_user: AuthenticatedUser = Depends(
            get_current_user
        ),
    ) -> AuthenticatedUser:

        permission_key = build_permission_key(
            module=module,
            action=action,
        )

        if not current_user.has_permission(
            permission_key
        ):
            raise ForbiddenError(
                message=(
                    "You do not have permission "
                    "to perform this action."
                ),
                meta={
                    "required_permission": permission_key,
                },
            )

        return current_user

    return dependency