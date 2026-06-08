from app.core.errors.exceptions import HospitalNotFoundError
from app.domain.entities.hospital import HospitalUnit
from app.domain.repositories.hospital_repository import HospitalRepository


class ListUnitsByHospitalUseCase:
    """
    Use case for listing units of a hospital.
    """

    def __init__(self, hospital_repository: HospitalRepository):
        self.hospital_repository = hospital_repository

    def execute(self, hospital_id: int) -> list[HospitalUnit]:
        hospital = self.hospital_repository.get_hospital(hospital_id)

        if not hospital:
            raise HospitalNotFoundError(hospital_id)

        return self.hospital_repository.list_units(hospital_id)