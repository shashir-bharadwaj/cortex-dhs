from sqlalchemy.orm import Session

from app.domain.entities.role_permission import RolePermission
from app.domain.repositories.role_permission_repository import (
    RolePermissionRepository,
)
from app.infrastructure.database.mappers.role_permission_mapper import (
    RolePermissionMapper,
)
from app.infrastructure.database.models.permission import PermissionModel
from app.infrastructure.database.models.role_permission import (
    RolePermissionModel,
)


class SQLAlchemyRolePermissionRepository(RolePermissionRepository):
    """
    SQLAlchemy implementation for role-permission assignments.
    """

    def __init__(self, db: Session):
        self.db = db

    def assign_permission(
        self,
        role_permission: RolePermission,
    ) -> RolePermission:
        """
        Assign a permission to a role.
        """
        model = RolePermissionMapper.to_model(role_permission)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return RolePermissionMapper.to_domain(model)

    def remove_permission(
        self,
        role_id: int,
        permission_id: int,
    ) -> None:
        """
        Remove a permission from a role.
        """
        (
            self.db.query(RolePermissionModel)
            .filter(
                RolePermissionModel.role_id == role_id,
                RolePermissionModel.permission_id == permission_id,
            )
            .delete()
        )

        self.db.commit()

    def list_by_role(self, role_id: int) -> list[RolePermission]:
        """
        List all raw permission mappings for a role.
        """
        models = (
            self.db.query(RolePermissionModel)
            .filter(RolePermissionModel.role_id == role_id)
            .all()
        )

        return RolePermissionMapper.to_domain_list(models)

    def permissions_by_role(
        self,
        role_id: int,
    ) -> dict[str, list[str]]:
        """
        Return permissions grouped by module for UI authorization.

        This method resolves RolePermission mappings into Permission
        module/action values.
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

    def role_has_permission(
        self,
        role_id: int,
        permission_key: str,
    ) -> bool:
        """
        Check whether role has a permission like PATIENTS:CREATE.
        """
        try:
            module, action = permission_key.split(":")
        except ValueError:
            return False

        exists = (
            self.db.query(RolePermissionModel)
            .join(
                PermissionModel,
                PermissionModel.id == RolePermissionModel.permission_id,
            )
            .filter(
                RolePermissionModel.role_id == role_id,
                PermissionModel.module == module,
                PermissionModel.action == action,
            )
            .first()
        )

        return exists is not None

    def replace_permissions(
        self,
        role_id: int,
        permission_ids: list[int],
    ) -> None:
        """
        Replace all permissions assigned to a role.
        """
        (
            self.db.query(RolePermissionModel)
            .filter(RolePermissionModel.role_id == role_id)
            .delete()
        )

        for permission_id in permission_ids:
            self.db.add(
                RolePermissionModel(
                    role_id=role_id,
                    permission_id=permission_id,
                )
            )

        self.db.commit()