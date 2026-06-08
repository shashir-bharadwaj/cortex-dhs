from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.authenticated_user import AuthenticatedUser
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.mappers.user_mapper import UserMapper
from app.infrastructure.database.models.role import RoleModel
from app.infrastructure.database.models.role_permission import RolePermissionModel
from app.infrastructure.database.models.user import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation for user persistence and authentication context loading.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        model = UserMapper.to_model(user)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self.by_id(model.id)

    def by_id(self, user_id: int) -> Optional[User]:
        model = (
            self.db.query(UserModel)
            .options(joinedload(UserModel.role))
            .filter(UserModel.id == user_id)
            .first()
        )

        if not model:
            return None

        return UserMapper.to_domain(model)

    def get_by_user_id(self, user_id: str) -> Optional[User]:
        model = (
            self.db.query(UserModel)
            .options(joinedload(UserModel.role))
            .filter(UserModel.user_id == user_id)
            .first()
        )

        if not model:
            return None

        return UserMapper.to_domain(model)

    def get_by_email(self, email: str) -> Optional[User]:
        model = (
            self.db.query(UserModel)
            .options(joinedload(UserModel.role))
            .filter(UserModel.email == email)
            .first()
        )

        if not model:
            return None

        return UserMapper.to_domain(model)

    def list(
        self,
        hospital_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        role_id: Optional[int] = None,
    ) -> List[User]:
        query = self.db.query(UserModel).options(joinedload(UserModel.role))

        if hospital_id is not None:
            query = query.filter(UserModel.hospital_id == hospital_id)

        if unit_id is not None:
            query = query.filter(UserModel.unit_id == unit_id)

        if role_id is not None:
            query = query.filter(UserModel.role_id == role_id)

        models = query.order_by(UserModel.id.desc()).all()

        return UserMapper.to_domain_list(models)

    def update(self, user: User) -> User:
        model = (
            self.db.query(UserModel)
            .filter(UserModel.id == user.id)
            .first()
        )

        if not model:
            raise ResourceNotFoundError(
                message="User not found.",
                meta={"user_id": user.id},
            )

        model.user_id = user.user_id
        model.first_name = user.first_name
        model.last_name = user.last_name
        model.email = user.email
        model.password_hash = user.password_hash
        model.role_id = user.role_id
        model.hospital_id = user.hospital_id
        model.unit_id = user.unit_id
        model.shift = (
            user.shift.value
            if hasattr(user.shift, "value")
            else user.shift
        )
        model.is_active = user.is_active

        self.db.commit()
        self.db.refresh(model)

        return self.by_id(model.id)

    def delete(self, user_id: int) -> None:
        model = (
            self.db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )

        if not model:
            raise ResourceNotFoundError(
                message="User not found.",
                meta={"user_id": user_id},
            )

        model.is_active = False

        self.db.commit()

    def get_auth_context_by_user_id(
        self,
        user_id: str,
    ) -> Optional[AuthenticatedUser]:
        """
        Load authenticated user context including role permissions.
        """
        model = (
            self.db.query(UserModel)
            .options(
                joinedload(UserModel.role)
                .joinedload(RoleModel.role_permissions)
                .joinedload(RolePermissionModel.permission)
            )
            .filter(UserModel.user_id == user_id)
            .first()
        )

        if not model:
            return None

        permissions = {
            f"{role_permission.permission.module}:"
            f"{role_permission.permission.action}"
            for role_permission in model.role.role_permissions
            if role_permission.permission is not None
        }

        return AuthenticatedUser(
            id=model.id,
            user_id=model.user_id,
            email=model.email,
            role_id=model.role_id,
            role_name=model.role.name,
            hospital_id=model.hospital_id,
            unit_id=model.unit_id,
            is_active=model.is_active,
            permissions=permissions,
        )

    # -----------------------------------------------------
    # Backward-compatible aliases
    # -----------------------------------------------------

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.by_id(user_id)

    def list_users(
        self,
        hospital_id: Optional[int] = None,
        unit_id: Optional[int] = None,
        role_id: Optional[int] = None,
    ) -> List[User]:
        return self.list(
            hospital_id=hospital_id,
            unit_id=unit_id,
            role_id=role_id,
        )