from fastapi import Depends

from app.api.providers.auth import get_current_user
from app.api.providers.db import DBProvider
from app.core.errors.exceptions import ForbiddenError
from app.domain.entities.user import User
from app.infrastructure.repositories.sqlalchemy_role_permission_repository import (
    SQLAlchemyRolePermissionRepository,
)


def require_permission(permission_key: str):
    """
    FastAPI dependency factory for permission-based authorization.

    Example:
    --------
    Depends(require_permission("patients:create"))
    """

    def dependency(
        current_user: User = Depends(get_current_user),
        db=Depends(DBProvider.get_db_session),
    ) -> User:
        repository = SQLAlchemyRolePermissionRepository(db)

        has_permission = repository.role_has_permission(
            role_id=current_user.role_id,
            permission_key=permission_key,
        )

        if not has_permission:
            raise ForbiddenError(
                message=f"Missing required permission: {permission_key}"
            )

        return current_user

    return dependency