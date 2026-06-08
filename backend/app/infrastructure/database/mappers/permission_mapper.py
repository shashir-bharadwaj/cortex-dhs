from typing import List

from app.domain.entities.permission import Permission
from app.infrastructure.database.models.permission import (
    PermissionModel,
)


class PermissionMapper:
    """
    Mapper responsible for converting Permission domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: PermissionModel,
    ) -> Permission:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        return Permission(
            id=model.id,
            module=model.module,
            action=model.action,
            description=model.description,
        )

    @staticmethod
    def to_model(
        entity: Permission,
    ) -> PermissionModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return PermissionModel(
            id=entity.id,
            module=entity.module,
            action=entity.action,
            description=entity.description,
        )

    @staticmethod
    def to_domain_list(
        models: List[PermissionModel],
    ) -> List[Permission]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            PermissionMapper.to_domain(model)
            for model in models
        ]