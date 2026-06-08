from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities.permission import Permission
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)
from app.domain.repositories.permission_repository import (
    PermissionRepository,
)
from app.infrastructure.database.mappers.permission_mapper import (
    PermissionMapper,
)
from app.infrastructure.database.models.permission import PermissionModel


class SQLAlchemyPermissionRepository(PermissionRepository):
    """
    SQLAlchemy implementation for permission persistence.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        permission: Permission,
    ) -> Permission:
        """
        Persist a new permission.
        """
        model = PermissionMapper.to_model(permission)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return PermissionMapper.to_domain(model)

    def get_by_id(
        self,
        permission_id: int,
    ) -> Optional[Permission]:
        """
        Retrieve permission by id.
        """
        model = (
            self.db.query(PermissionModel)
            .filter(PermissionModel.id == permission_id)
            .first()
        )

        if not model:
            return None

        return PermissionMapper.to_domain(model)

    def get_by_module_action(
        self,
        module: PermissionModule,
        action: PermissionAction,
    ) -> Optional[Permission]:
        """
        Retrieve permission by module and action.
        """
        model = (
            self.db.query(PermissionModel)
            .filter(
                PermissionModel.module == module,
                PermissionModel.action == action,
            )
            .first()
        )

        if not model:
            return None

        return PermissionMapper.to_domain(model)

    def list(self) -> list[Permission]:
        """
        List all permissions.
        """
        models = (
            self.db.query(PermissionModel)
            .order_by(
                PermissionModel.module.asc(),
                PermissionModel.action.asc(),
            )
            .all()
        )

        return PermissionMapper.to_domain_list(models)