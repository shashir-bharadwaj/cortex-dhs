from typing import List

from app.domain.entities.user import User
from app.infrastructure.database.models.user import UserModel


class UserMapper:
    """
    Mapper responsible for converting User domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: UserModel,
    ) -> User:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        role_name = (
            model.role.name
            if getattr(model, "role", None)
            else None
        )

        return User(
            id=model.id,
            user_id=model.user_id,
            first_name=model.first_name,
            last_name=model.last_name,
            email=model.email,
            password_hash=model.password_hash,
            role_id=model.role_id,
            hospital_id=model.hospital_id,
            unit_id=model.unit_id,
            shift=model.shift,
            is_active=model.is_active,
            role=role_name,
        )

    @staticmethod
    def to_model(
        entity: User,
    ) -> UserModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return UserModel(
            id=entity.id,
            user_id=entity.user_id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            password_hash=entity.password_hash,
            role_id=entity.role_id,
            hospital_id=entity.hospital_id,
            unit_id=entity.unit_id,
            shift=(
                entity.shift.value
                if hasattr(entity.shift, "value")
                else entity.shift
            ),
            is_active=entity.is_active,
        )

    @staticmethod
    def to_domain_list(
        models: List[UserModel],
    ) -> List[User]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            UserMapper.to_domain(model)
            for model in models
        ]