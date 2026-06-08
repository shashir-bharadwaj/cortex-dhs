from app.core.errors.exceptions import HospitalUnitNotFoundError
from app.domain.entities.hospital import HospitalUnit
from app.domain.repositories.hospital_repository import HospitalRepository


class GetHospitalUnitUseCase:
    """
    Use case for retrieving a hospital unit by id.
    """

    def __init__(self, hospital_repository: HospitalRepository):
        self.hospital_repository = hospital_repository

    def execute(self, unit_id: int) -> HospitalUnit:
        unit = self.hospital_repository.get_unit(unit_id)

        if not unit:
            raise HospitalUnitNotFoundError(unit_id)

        return unit