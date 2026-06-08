"""
Auth API endpoints.

This module exposes authentication-related endpoints such as:
- login
- logout
- current authenticated user
- shift update for current user
"""

from fastapi import APIRouter, Depends, Response, status

from app.api.providers.auth import AuthProvider
from app.api.providers.db import DBProvider
from sqlalchemy.orm import Session
from app.api.schemas.auth import (
    AuthUserResponse,
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
    UpdateShiftRequest,
    UpdateShiftResponse,
)
from app.application.auth.use_cases.get_current_user import GetCurrentUserUseCase
from app.application.auth.use_cases.login import LoginUseCase
from app.application.auth.use_cases.logout import LogoutUseCase
from app.application.auth.use_cases.update_shift import UpdateShiftUseCase
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.entities.user import User
from app.infrastructure.database.models.permission import PermissionModel
from app.infrastructure.database.models.role_permission import RolePermissionModel
from app.infrastructure.repositories.sqlalchemy_role_permission_repository import SQLAlchemyRolePermissionRepository
from app.infrastructure.security.auth_dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


def to_auth_user_response(user: User) -> AuthUserResponse:
    """
    Map a domain User entity to the auth user response schema.
    """

    return AuthUserResponse(
        id=user.id,
        userId=user.user_id,
        firstName=user.first_name,
        lastName=user.last_name,
        email=user.email,
        roleId=user.role_id,
        hospitalId=user.hospital_id,
        unitId=user.unit_id,
        shift=user.shift,
        isActive=user.is_active,
)


def to_current_user_response(
        user: User,
        permissions: dict[str, list[str]],
    ) -> CurrentUserResponse:
    """
    Map a domain User entity to the current-user response schema.
    """

    return CurrentUserResponse(
        id=user.id,

        userId=user.user_id,

        firstName=user.first_name,
        lastName=user.last_name,

        email=user.email,

        roleId=user.role_id,

        hospitalId=user.hospital_id,
        unitId=user.unit_id,

        shift=user.shift,

        isActive=user.is_active,

        permissions=permissions,
    )


def permissions_by_role(
    self,
    role_id: int,
) -> dict[str, list[str]]:
    """
    Return permissions grouped by module for UI authorization.
    """

    rows = (
        self.db.query(
            PermissionModel.module,
            PermissionModel.action,
        )
        .join(
            RolePermissionModel,
            RolePermissionModel.permission_id == PermissionModel.id,
        )
        .filter(RolePermissionModel.role_id == role_id)
        .order_by(
            PermissionModel.module.asc(),
            PermissionModel.action.asc(),
        )
        .all()
    )

    permissions: dict[str, list[str]] = {}

    for module, action in rows:
        permissions.setdefault(module, []).append(action)

    return permissions

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def login(
    payload: LoginRequest,
    use_case: LoginUseCase = Depends(AuthProvider.login_use_case),
) -> LoginResponse:
    """
    Authenticate a user using user ID and password.

    The use case loads the full user context from the database,
    verifies the password, and returns the issued token together
    with the authenticated user entity.
    """
    token, user = use_case.execute(payload.email, payload.password)

    return LoginResponse(
        token=token,
        user=to_auth_user_response(user),
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def logout(
    _current_user=Depends(get_current_user),
    use_case: LogoutUseCase = Depends(AuthProvider.logout_use_case),
):
    """
    Log out the current authenticated user.

    Current implementation is stateless, so logout mainly exists
    as an API contract hook for frontend/session workflows.

    Frontend should discard the JWT token locally after logout.
    """
    use_case.execute()

    return {
        "message": "Logged out successfully"
    }


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def me(
    current_user=Depends(get_current_user),
    db: Session = Depends(DBProvider.get_db_session),
    use_case: GetCurrentUserUseCase = Depends(AuthProvider.current_user_use_case),
) -> CurrentUserResponse:
    """
    Return the currently authenticated user.
    """
    user = use_case.execute(current_user)


    permissions = SQLAlchemyRolePermissionRepository(
        db
    ).permissions_by_role(user.role_id)

    return to_current_user_response(
        user=user,
        permissions=permissions,
    )


@router.put(
    "/me/shift",
    response_model=UpdateShiftResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def update_shift(
    payload: UpdateShiftRequest,
    current_user=Depends(get_current_user),
    use_case: UpdateShiftUseCase = Depends(AuthProvider.update_shift_use_case),
) -> UpdateShiftResponse:
    """
    Update the current user's shift and unit assignment.
    """
    user = use_case.execute(current_user, payload)

    return UpdateShiftResponse(
        shift=user.shift,
        unitId=user.unit_id,
    )