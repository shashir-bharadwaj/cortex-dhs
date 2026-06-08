from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.vital import Vital
from app.domain.repositories.vital_repository import VitalRepository


class GetVitalUseCase:
    """
    Use case for reading a single vital record.
    """

    def __init__(self, vital_repository: VitalRepository):
        self.vital_repository = vital_repository

    def execute(self, vital_id: int) -> Vital:
        vital = self.vital_repository.by_id(vital_id)

        if not vital:
            raise ResourceNotFoundError(
                message="Vital record not found.",
                meta={"vital_id": vital_id},
            )

        return vital