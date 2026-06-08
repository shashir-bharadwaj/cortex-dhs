from app.domain.entities.hospital import Hospital
from app.domain.repositories.hospital_repository import HospitalRepository


class CreateHospitalUseCase:
    """
    Use case for creating a hospital.
    """

    def __init__(self, hospital_repository: HospitalRepository):
        self.hospital_repository = hospital_repository

    def execute(
        self,
        name: str,
        code: str | None = None,
        address: str | None = None,
        city: str | None = None,
        state: str | None = None,
        country: str | None = None,
        contact_number: str | None = None,
        email: str | None = None,
    ) -> Hospital:
        hospital = Hospital(
            id=None,
            name=name,
            code=code,
            address=address,
            city=city,
            state=state,
            country=country,
            contact_number=contact_number,
            email=email,
        )

        return self.hospital_repository.create_hospital(hospital)