from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.role import Role
from app.domain.repositories.role_repository import RoleRepository
from app.infrastructure.database.mappers.role_mapper import RoleMapper
from app.infrastructure.database.models.role import RoleModel


class SQLAlchemyRoleRepository(RoleRepository):
    """
    SQLAlchemy implementation for role persistence.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, role: Role) -> Role:
        """
        Persist a new role.
        """
        model = RoleMapper.to_model(role)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return RoleMapper.to_domain(model)

    def by_id(self, role_id: int) -> Optional[Role]:
        """
        Retrieve role by id.
        """
        model = (
            self.db.query(RoleModel)
            .filter(RoleModel.id == role_id)
            .first()
        )

        if not model:
            return None

        return RoleMapper.to_domain(model)

    def by_name(self, name: str) -> Optional[Role]:
        """
        Retrieve role by name.
        """
        model = (
            self.db.query(RoleModel)
            .filter(RoleModel.name == name)
            .first()
        )

        if not model:
            return None

        return RoleMapper.to_domain(model)

    def list(self) -> List[Role]:
        """
        List all roles.
        """
        models = (
            self.db.query(RoleModel)
            .order_by(RoleModel.id.asc())
            .all()
        )

        return RoleMapper.to_domain_list(models)

    def update(self, role: Role) -> Role:
        """
        Update an existing role.
        """
        model = (
            self.db.query(RoleModel)
            .filter(RoleModel.id == role.id)
            .first()
        )

        if not model:
            raise ValueError("Role not found")

        model.name = role.name
        model.description = role.description

        self.db.commit()
        self.db.refresh(model)

        return RoleMapper.to_domain(model)

    def delete(self, role_id: int) -> None:
        """
        Delete a role.
        """
        model = (
            self.db.query(RoleModel)
            .filter(RoleModel.id == role_id)
            .first()
        )

        if not model:
            raise ValueError("Role not found")

        self.db.delete(model)
        self.db.commit()

    # -----------------------------------------------------
    # Backward-compatible aliases
    # -----------------------------------------------------

    def get_by_id(self, role_id: int) -> Optional[Role]:
        """
        Compatibility alias.
        """
        return self.by_id(role_id)

    def list_roles(self) -> List[Role]:
        """
        Compatibility alias.
        """
        return self.list()