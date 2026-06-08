from app.domain.repositories.permission_repository import PermissionRepository
from app.domain.repositories.role_permission_repository import (
    RolePermissionRepository,
)
from app.domain.repositories.role_repository import RoleRepository


MODULE_LABELS = {
    "ALARMS": "Alarms",
    "BED_MANAGEMENT": "Bed Management",
    "DEVICE_MANAGEMENT": "Device Management",
    "HOSPITALS": "Hospitals",
    "ICU_MANAGEMENT": "ICU Management",
    "MANAGE_USERS": "Manage Users",
    "PATIENTS": "Patients",
    "TIMELINE": "Timeline",
    "VITALS": "Vitals",
}


class ListPermissionsUseCase:
    """
    Use case for listing permissions in a frontend-friendly role matrix.

    Output shape:
    - role
    - modules
    - allowed actions per module
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

    def execute(self) -> list[dict]:
        roles = self.role_repository.list()
        permissions = self.permission_repository.list()

        modules = sorted({permission.module for permission in permissions})

        result = []

        for role in roles:
            assigned_permissions = (
                self.role_permission_repository.permissions_by_role(role.id)
            )

            module_permissions = []

            for module in modules:
                allowed_actions = sorted(
                    assigned_permissions.get(module, [])
                )

                module_permissions.append(
                    {
                        "module": module,
                        "moduleName": MODULE_LABELS.get(
                            module,
                            module.replace("_", " ").title(),
                        ),
                        "allowedActions": allowed_actions,
                    }
                )

            result.append(
                {
                    "roleId": role.id,
                    "role": role.name,
                    "permissions": module_permissions,
                }
            )

        return result