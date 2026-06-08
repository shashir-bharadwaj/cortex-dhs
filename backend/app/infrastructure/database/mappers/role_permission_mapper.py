from typing import List

from app.domain.entities.role_permission import RolePermission
from app.infrastructure.database.models.role_permission import (
    RolePermissionModel,
)


class RolePermissionMapper:
    """
    Mapper responsible for converting RolePermission domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: RolePermissionModel,
    ) -> RolePermission:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        return RolePermission(
            id=model.id,
            role_id=model.role_id,
            permission_id=model.permission_id,
        )

    @staticmethod
    def to_model(
        entity: RolePermission,
    ) -> RolePermissionModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return RolePermissionModel(
            id=entity.id,
            role_id=entity.role_id,
            permission_id=entity.permission_id,
        )

    @staticmethod
    def to_domain_list(
        models: List[RolePermissionModel],
    ) -> List[RolePermission]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            RolePermissionMapper.to_domain(model)
            for model in models
        ]