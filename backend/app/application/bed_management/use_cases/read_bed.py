from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.bed import BedMaster
from app.domain.repositories.bed_repository import BedRepository


class ReadBedUseCase:
    """
    Use case for reading a single bed.
    """

    def __init__(self, bed_repository: BedRepository):
        self.bed_repository = bed_repository

    def execute(self, bed_record_id: int) -> BedMaster:
        bed = self.bed_repository.by_id(bed_record_id)

        if not bed:
            raise ResourceNotFoundError(
                message="Bed not found.",
                meta={"bed_record_id": bed_record_id},
            )

        return bed