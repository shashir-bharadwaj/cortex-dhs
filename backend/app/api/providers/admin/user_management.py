from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.user_management.use_cases.change_user_role import (
    ChangeUserRoleUseCase,
)
from app.application.user_management.use_cases.create_role import CreateRoleUseCase
from app.application.user_management.use_cases.create_user import (
    CreateUserUseCase,
)
from app.application.user_management.use_cases.delete_user import (
    DeleteUserUseCase,
)
from app.application.user_management.use_cases.list_permissions import (
    ListPermissionsUseCase,
)
from app.application.user_management.use_cases.list_roles import (
    ListRolesUseCase,
)
from app.application.user_management.use_cases.list_users import (
    ListUsersUseCase,
)
from app.application.user_management.use_cases.reset_user_password import (
    ResetUserPasswordUseCase,
)
from app.application.user_management.use_cases.update_role_permissions import (
    UpdateRolePermissionsUseCase,
)
from app.application.user_management.use_cases.update_user import (
    UpdateUserUseCase,
)
from app.application.user_management.use_cases.update_user_status import (
    UpdateUserStatusUseCase,
)
from app.domain.repositories.permission_repository import (
    PermissionRepository,
)
from app.domain.repositories.role_permission_repository import (
    RolePermissionRepository,
)
from app.domain.repositories.role_repository import (
    RoleRepository,
)
from app.domain.repositories.user_repository import (
    UserRepository,
)


class UserManagementProvider:
    """
    Dependency provider for the User Management module.

    Responsibility:
    ----------------
    Construct and wire user-management-related use cases.

    Why this layer exists:
    ----------------------
    Endpoints should not directly construct repositories or use cases.
    This provider centralizes dependency injection and keeps route
    handlers thin and maintainable.

    Architectural benefit:
    ----------------------
    Use cases depend only on domain repository interfaces, while
    RepositoryProvider decides which concrete SQLAlchemy repository
    implementation should be injected.
    """

    @staticmethod
    def create_user_use_case(
        user_repository: UserRepository = Depends(
            RepositoryProvider.get_user_repository
        ),
        role_repository: RoleRepository = Depends(
            RepositoryProvider.get_role_repository
        ),
    ) -> CreateUserUseCase:
        """
        Provide CreateUserUseCase with required repositories.
        """
        return CreateUserUseCase(
            user_repository=user_repository,
            role_repository=role_repository,
        )

    @staticmethod
    def list_users_use_case(
        user_repository: UserRepository = Depends(
            RepositoryProvider.get_user_repository
        ),
    ) -> ListUsersUseCase:
        """
        Provide ListUsersUseCase.
        """
        return ListUsersUseCase(
            user_repository=user_repository,
        )

    @staticmethod
    def list_roles_use_case(
        role_repository: RoleRepository = Depends(
            RepositoryProvider.get_role_repository
        ),
    ) -> ListRolesUseCase:
        """
        Provide ListRolesUseCase.
        """
        return ListRolesUseCase(
            role_repository=role_repository,
        )

    @staticmethod
    def list_permissions_use_case(
        role_repository: RoleRepository = Depends(
            RepositoryProvider.get_role_repository
        ),
        permission_repository: PermissionRepository = Depends(
            RepositoryProvider.get_permission_repository
        ),
        role_permission_repository: RolePermissionRepository = Depends(
            RepositoryProvider.get_role_permission_repository
        ),
    ) -> ListPermissionsUseCase:
        """
        Provide ListPermissionsUseCase.

        Returns frontend-friendly permission matrix grouped by:
        - role
        - module
        - allowed actions
        """
        return ListPermissionsUseCase(
            role_repository=role_repository,
            permission_repository=permission_repository,
            role_permission_repository=role_permission_repository,
        )

    @staticmethod
    def update_user_use_case(
        user_repository: UserRepository = Depends(
            RepositoryProvider.get_user_repository
        ),
        role_repository: RoleRepository = Depends(
            RepositoryProvider.get_role_repository
        ),
    ) -> UpdateUserUseCase:
        """
        Provide UpdateUserUseCase.
        """
        return UpdateUserUseCase(
            user_repository=user_repository,
            role_repository=role_repository,
        )

    @staticmethod
    def update_user_status_use_case(
        user_repository: UserRepository = Depends(
            RepositoryProvider.get_user_repository
        ),
    ) -> UpdateUserStatusUseCase:
        """
        Provide UpdateUserStatusUseCase.
        """
        return UpdateUserStatusUseCase(
            user_repository=user_repository
        )

    @staticmethod
    def reset_user_password_use_case(
        user_repository: UserRepository = Depends(
            RepositoryProvider.get_user_repository
        ),
    ) -> ResetUserPasswordUseCase:
        """
        Provide ResetUserPasswordUseCase.
        """
        return ResetUserPasswordUseCase(
            user_repository=user_repository
        )

    @staticmethod
    def change_user_role_use_case(
        user_repository: UserRepository = Depends(
            RepositoryProvider.get_user_repository
        ),
        role_repository: RoleRepository = Depends(
            RepositoryProvider.get_role_repository
        ),
    ) -> ChangeUserRoleUseCase:
        """
        Provide ChangeUserRoleUseCase.
        """
        return ChangeUserRoleUseCase(
            user_repository=user_repository,
            role_repository=role_repository,
        )

    @staticmethod
    def update_role_permissions_use_case(
        role_repository: RoleRepository = Depends(
            RepositoryProvider.get_role_repository
        ),
        permission_repository: PermissionRepository = Depends(
            RepositoryProvider.get_permission_repository
        ),
        role_permission_repository: RolePermissionRepository = Depends(
            RepositoryProvider.get_role_permission_repository
        ),
    ) -> UpdateRolePermissionsUseCase:
        """
        Provide UpdateRolePermissionsUseCase.
        """
        return UpdateRolePermissionsUseCase(
            role_repository=role_repository,
            permission_repository=permission_repository,
            role_permission_repository=role_permission_repository,
        )

    @staticmethod
    def delete_user_use_case(
        user_repository: UserRepository = Depends(
            RepositoryProvider.get_user_repository
        ),
    ) -> DeleteUserUseCase:
        """
        Provide DeleteUserUseCase.
        """
        return DeleteUserUseCase(
            user_repository=user_repository
        )
    
    @staticmethod
    def create_role_use_case(
        role_repository: RoleRepository = Depends(
            RepositoryProvider.get_role_repository
        ),
        permission_repository: PermissionRepository = Depends(
            RepositoryProvider.get_permission_repository
        ),
        role_permission_repository: RolePermissionRepository = Depends(
            RepositoryProvider.get_role_permission_repository
        ),
    ) -> CreateRoleUseCase:
        """
        Provide CreateRoleUseCase.
        """
        return CreateRoleUseCase(
            role_repository=role_repository,
            permission_repository=permission_repository,
            role_permission_repository=role_permission_repository,
        )