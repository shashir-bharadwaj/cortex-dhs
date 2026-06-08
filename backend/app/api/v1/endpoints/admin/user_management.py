from fastapi import APIRouter, Depends, status

from app.api.providers.admin.user_management import UserManagementProvider
from app.api.providers.auth import AuthProvider
from app.api.schemas.role import RoleCreateRequest, RoleResponse
from app.api.schemas.user import (
    RolePermissionMatrixListResponse,
    RolePermissionsUpdateRequest,
    UserCreateRequest,
    UserPasswordResetRequest,
    UserResponse,
    UserRoleUpdateRequest,
    UserStatusUpdateRequest,
    UserUpdateRequest,
)
from app.application.user_management.use_cases.change_user_role import (
    ChangeUserRoleUseCase,
)
from app.application.user_management.use_cases.create_role import CreateRoleUseCase
from app.application.user_management.use_cases.create_user import CreateUserUseCase
from app.application.user_management.use_cases.delete_user import DeleteUserUseCase
from app.application.user_management.use_cases.list_permissions import (
    ListPermissionsUseCase,
)
from app.application.user_management.use_cases.list_roles import ListRolesUseCase
from app.application.user_management.use_cases.list_users import ListUsersUseCase
from app.application.user_management.use_cases.reset_user_password import (
    ResetUserPasswordUseCase,
)
from app.application.user_management.use_cases.update_role_permissions import (
    UpdateRolePermissionsUseCase,
)
from app.application.user_management.use_cases.update_user import UpdateUserUseCase
from app.application.user_management.use_cases.update_user_status import (
    UpdateUserStatusUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.entities.user import User
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin - User Management"],
)


def manage_users_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for User Management routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.MANAGE_USERS,
            action,
        )
    )


def to_user_response(user: User) -> UserResponse:
    """
    Convert User domain entity into API response schema.
    """
    return UserResponse(
        id=user.id,
        userId=user.user_id,
        firstName=user.first_name,
        lastName=user.last_name,
        email=user.email,
        roleId=user.role_id,
        role=user.role,
        hospitalId=user.hospital_id,
        unitId=user.unit_id,
        shift=user.shift,
        isActive=user.is_active,
    )


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_user(
    payload: UserCreateRequest,
    _current_user=manage_users_permission(PermissionAction.CREATE),
    use_case: CreateUserUseCase = Depends(
        UserManagementProvider.create_user_use_case
    ),
) -> UserResponse:
    """
    Create a new platform user.
    """
    generated_user_id = (
        f"{payload.first_name.lower()}."
        f"{payload.last_name.lower()}"
    )

    user = User(
        user_id=generated_user_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password_hash="",
        role_id=payload.role_id,
        hospital_id=payload.hospital_id,
        unit_id=payload.unit_id,
        shift=payload.shift,
    )

    created_user = use_case.execute(
        user=user,
        password=payload.password,
    )

    return to_user_response(created_user)


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_users(
    _current_user=manage_users_permission(PermissionAction.VIEW),
    use_case: ListUsersUseCase = Depends(
        UserManagementProvider.list_users_use_case
    ),
) -> list[UserResponse]:
    """
    List all platform users.
    """
    users = use_case.execute()

    return [to_user_response(user) for user in users]


@router.get(
    "/roles",
    response_model=list[RoleResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_roles(
    _current_user=manage_users_permission(PermissionAction.VIEW),
    use_case: ListRolesUseCase = Depends(
        UserManagementProvider.list_roles_use_case
    ),
) -> list[RoleResponse]:
    """
    List available roles for assigning users.
    """
    return use_case.execute()

@router.post(
    "/roles",
    response_model=RolePermissionMatrixListResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_role(
    payload: RoleCreateRequest,
    _current_user=manage_users_permission(PermissionAction.CREATE),
    create_use_case: CreateRoleUseCase = Depends(
        UserManagementProvider.create_role_use_case
    ),
    list_use_case: ListPermissionsUseCase = Depends(
        UserManagementProvider.list_permissions_use_case
    ),
) -> RolePermissionMatrixListResponse:
    """
    Create a new role with permissions.
    """
    create_use_case.execute(
        name=payload.name,
        description=payload.description,
        permissions_payload=payload.permissions,
    )

    return {
        "rolePermissions": list_use_case.execute(),
    }


@router.get(
    "/permissions",
    response_model=RolePermissionMatrixListResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_permissions(
    _current_user=manage_users_permission(PermissionAction.VIEW),
    use_case: ListPermissionsUseCase = Depends(
        UserManagementProvider.list_permissions_use_case
    ),
) -> RolePermissionMatrixListResponse:
    """
    Return frontend-friendly role permission matrix.
    """
    return {
        "rolePermissions": use_case.execute(),
    }


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    _current_user=manage_users_permission(PermissionAction.MODIFY),
    use_case: UpdateUserUseCase = Depends(
        UserManagementProvider.update_user_use_case
    ),
) -> UserResponse:
    """
    Update user profile, role, hospital/unit mapping,
    shift, and active status.
    """
    updated_user = use_case.execute(user_id, payload)

    return to_user_response(updated_user)


@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def update_user_status(
    user_id: int,
    payload: UserStatusUpdateRequest,
    _current_user=manage_users_permission(PermissionAction.MODIFY),
    use_case: UpdateUserStatusUseCase = Depends(
        UserManagementProvider.update_user_status_use_case
    ),
) -> UserResponse:
    """
    Activate or deactivate a user account.
    """
    updated_user = use_case.execute(
        user_id=user_id,
        is_active=payload.is_active,
    )

    return to_user_response(updated_user)


@router.patch(
    "/{user_id}/password",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def reset_user_password(
    user_id: int,
    payload: UserPasswordResetRequest,
    _current_user=manage_users_permission(PermissionAction.MODIFY),
    use_case: ResetUserPasswordUseCase = Depends(
        UserManagementProvider.reset_user_password_use_case
    ),
) -> UserResponse:
    """
    Reset a user's password.
    """
    updated_user = use_case.execute(
        user_id=user_id,
        password=payload.password,
    )

    return to_user_response(updated_user)


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def change_user_role(
    user_id: int,
    payload: UserRoleUpdateRequest,
    _current_user=manage_users_permission(PermissionAction.MODIFY),
    use_case: ChangeUserRoleUseCase = Depends(
        UserManagementProvider.change_user_role_use_case
    ),
) -> UserResponse:
    """
    Change a user's assigned role.
    """
    updated_user = use_case.execute(
        user_id=user_id,
        role_id=payload.role_id,
    )

    return to_user_response(updated_user)


@router.put(
    "/roles/{role_id}/permissions",
    response_model=RolePermissionMatrixListResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def update_role_permissions(
    role_id: int,
    payload: RolePermissionsUpdateRequest,
    _current_user=manage_users_permission(PermissionAction.MODIFY),
    update_use_case: UpdateRolePermissionsUseCase = Depends(
        UserManagementProvider.update_role_permissions_use_case
    ),
    list_use_case: ListPermissionsUseCase = Depends(
        UserManagementProvider.list_permissions_use_case
    ),
) -> RolePermissionMatrixListResponse:
    """
    Replace permissions assigned to a role and return updated matrix.
    """
    update_use_case.execute(
        role_id=role_id,
        permissions_payload=payload.permissions,
    )

    return {
        "rolePermissions": list_use_case.execute(),
    }


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=STANDARD_ERROR_RESPONSES,
)
def delete_user(
    user_id: int,
    _current_user=manage_users_permission(PermissionAction.DELETE),
    use_case: DeleteUserUseCase = Depends(
        UserManagementProvider.delete_user_use_case
    ),
) -> None:
    """
    Soft-delete/deactivate a user.
    """
    use_case.execute(user_id)

    return None