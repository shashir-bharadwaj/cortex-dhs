# app/application/vitals/use_cases/upsert_latest_vital.py

from app.domain.entities.latest_vital import LatestVital
from app.domain.repositories.latest_vital_repository import (
    LatestVitalRepository,
)


class UpsertLatestVitalUseCase:
    """
    Use case responsible for maintaining the latest
    live vital snapshot of a patient.
    """

    def __init__(
        self,
        latest_vital_repository: LatestVitalRepository,
    ):
        self.latest_vital_repository = latest_vital_repository

    def execute(
        self,
        latest_vital: LatestVital,
    ) -> LatestVital:
        """
        Create or update latest patient vital snapshot.
        """
        return self.latest_vital_repository.upsert(latest_vital)