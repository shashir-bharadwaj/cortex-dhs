from typing import List

from app.domain.entities.role import Role
from app.infrastructure.database.models.role import RoleModel


class RoleMapper:
    """
    Mapper responsible for converting Role domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: RoleModel,
    ) -> Role:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        return Role(
            id=model.id,
            name=model.name,
            description=model.description,
        )

    @staticmethod
    def to_model(
        entity: Role,
    ) -> RoleModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return RoleModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
        )

    @staticmethod
    def to_domain_list(
        models: List[RoleModel],
    ) -> List[Role]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            RoleMapper.to_domain(model)
            for model in models
        ]