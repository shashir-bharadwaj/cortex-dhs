from app.core.errors.exceptions import HospitalNotFoundError
from app.domain.entities.hospital import HospitalUnit
from app.domain.repositories.hospital_repository import HospitalRepository


class CreateHospitalUnitUseCase:
    """
    Use case for creating a hospital unit.
    """

    def __init__(self, hospital_repository: HospitalRepository):
        self.hospital_repository = hospital_repository

    def execute(
        self,
        hospital_id: int,
        name: str,
        code: str | None = None,
    ) -> HospitalUnit:
        hospital = self.hospital_repository.get_hospital(hospital_id)
        if not hospital:
            raise HospitalNotFoundError(hospital_id)

        unit = HospitalUnit(
            id=None,
            hospital_id=hospital_id,
            name=name,
            code=code
        )

        return self.hospital_repository.create_unit(unit)