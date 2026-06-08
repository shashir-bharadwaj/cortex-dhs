from app.core.errors.exceptions import (
    ConflictError,
    ResourceNotFoundError,
)
from app.domain.entities.user import User
from app.domain.repositories.role_repository import RoleRepository
from app.domain.repositories.user_repository import UserRepository


class UpdateUserUseCase:
    """
    Use case for updating a user.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def execute(
        self,
        user_id: int,
        payload,
    ) -> User:
        existing_user = self.user_repository.by_id(user_id)

        if not existing_user:
            raise ResourceNotFoundError(
                message="User not found.",
                meta={"user_id": user_id},
            )

        role = self.role_repository.by_id(payload.role_id)

        if not role:
            raise ResourceNotFoundError(
                message="Role not found.",
                meta={"role_id": payload.role_id},
            )

        duplicate = self.user_repository.by_email(payload.email)

        if duplicate and duplicate.id != user_id:
            raise ConflictError(
                message="Email already exists.",
                meta={"email": payload.email},
            )

        updated_user = User(
            id=user_id,
            user_id=existing_user.user_id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            password_hash=existing_user.password_hash,
            role_id=payload.role_id,
            hospital_id=payload.hospital_id,
            unit_id=payload.unit_id,
            shift=payload.shift,
            is_active=payload.is_active,
        )

        return self.user_repository.update(updated_user)