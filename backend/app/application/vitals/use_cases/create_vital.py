from app.domain.entities.vital import Vital
from app.domain.repositories.vital_repository import VitalRepository


class CreateVitalUseCase:
    """
    Use case for creating a vital record.
    """

    def __init__(self, vital_repository: VitalRepository):
        self.vital_repository = vital_repository

    def execute(self, vital: Vital) -> Vital:
        return self.vital_repository.create(vital)