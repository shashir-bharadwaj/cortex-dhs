from app.domain.entities.user import User


class UpdateShiftUseCase:
    """
    Update current user's working shift and unit.
    """

    def __init__(self, user_repository) -> None:
        self.user_repository = user_repository

    def execute(self, current_user, payload):
        updated_user = User(
            id=current_user.id,
            user_id=current_user.user_id,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email,
            password_hash=current_user.password_hash,
            role_id=current_user.role_id,
            role=current_user.role,
            hospital_id=current_user.hospital_id,
            unit_id=payload.unitId,
            shift=payload.shift,
            is_active=current_user.is_active,
        )
        
        return self.user_repository.update(updated_user)
