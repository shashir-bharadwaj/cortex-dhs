from typing import List

from app.domain.entities.hospital import Hospital
from app.domain.repositories.hospital_repository import HospitalRepository


class ListHospitalsUseCase:
    """
    Use case for listing hospitals.
    """

    def __init__(self, repository: HospitalRepository):
        self.repository = repository

    def execute(self) -> List[Hospital]:
        return self.repository.list_hospitals()