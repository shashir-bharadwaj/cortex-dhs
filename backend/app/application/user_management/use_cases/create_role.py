from app.core.errors.exceptions import ConflictError, ResourceNotFoundError
from app.domain.entities.role import Role
from app.domain.entities.role_permission import RolePermission
from app.domain.repositories.permission_repository import (
    PermissionRepository,
)
from app.domain.repositories.role_permission_repository import (
    RolePermissionRepository,
)
from app.domain.repositories.role_repository import RoleRepository


class CreateRoleUseCase:
    """
    Use case for creating a new role with permissions.

    Frontend sends permissions grouped by module and actions.
    This use case resolves them into permission IDs and creates
    role-permission mappings.
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
        name: str,
        description: str | None,
        permissions_payload: list,
    ) -> Role:
        existing_role = self.role_repository.by_name(name)

        if existing_role:
            raise ConflictError(
                message="Role already exists.",
                meta={"role_name": name},
            )

        role = Role(
            name=name,
            description=description,
        )

        created_role = self.role_repository.create(role)

        all_permissions = self.permission_repository.list()

        permission_lookup = {
            f"{permission.module}:{permission.action}": permission.id
            for permission in all_permissions
        }

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

                self.role_permission_repository.assign_permission(
                    RolePermission(
                        role_id=created_role.id,
                        permission_id=permission_id,
                    )
                )

        return created_role