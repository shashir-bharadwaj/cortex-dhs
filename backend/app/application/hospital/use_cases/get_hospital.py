from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.hospital import Hospital
from app.domain.repositories.hospital_repository import HospitalRepository


class GetHospitalUseCase:
    """
    Use case for reading a hospital.
    """

    def __init__(self, repository: HospitalRepository):
        self.repository = repository

    def execute(self, hospital_id: int) -> Hospital:
        hospital = self.repository.get_hospital(hospital_id)

        if not hospital:
            raise ResourceNotFoundError(
                message="Hospital not found.",
                meta={"hospital_id": hospital_id},
            )

        return hospital