from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.permission_repository import PermissionRepository
from app.domain.repositories.role_permission_repository import (
    RolePermissionRepository,
)
from app.domain.repositories.role_repository import RoleRepository


class UpdateRolePermissionsUseCase:
    """
    Use case for replacing permissions assigned to a role.

    Input shape is frontend-friendly:
    [
        {
            "module": "PATIENTS",
            "allowedActions": ["VIEW", "CREATE"]
        }
    ]

    Internally, this use case converts module/action pairs back into
    permission IDs before updating role_permissions.
    """

    def __init__(
        self,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
    ):
        self.role_repository = role_repository
        self.permission_repository = permission_repository
        self.role_permission_repository = role_permission_repository

    def execute(
        self,
        role_id: int,
        permissions_payload: list,
    ) -> None:
        role = self.role_repository.by_id(role_id)

        if not role:
            raise ResourceNotFoundError(
                message="Role not found.",
                meta={"role_id": role_id},
            )

        all_permissions = self.permission_repository.list()

        permission_lookup = {
            f"{permission.module}:{permission.action}": permission.id
            for permission in all_permissions
        }

        permission_ids: list[int] = []

        for module_permission in permissions_payload:
            module = module_permission.module
            allowed_actions = module_permission.allowed_actions

            for action in allowed_actions:
                permission_key = f"{module}:{action}"

                permission_id = permission_lookup.get(permission_key)

                if permission_id is None:
                    raise ResourceNotFoundError(
                        message="Permission not found.",
                        meta={
                            "module": module,
                            "action": action,
                            "permission_key": permission_key,
                        },
                    )

                permission_ids.append(permission_id)

        self.role_permission_repository.replace_permissions(
            role_id=role_id,
            permission_ids=permission_ids,
        )