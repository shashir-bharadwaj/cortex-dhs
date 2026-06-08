from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.bed_repository import BedRepository


class DeleteBedUseCase:
    """
    Use case for deleting a bed.
    """

    def __init__(self, bed_repository: BedRepository):
        self.bed_repository = bed_repository

    def execute(self, bed_record_id: int) -> None:
        bed = self.bed_repository.by_id(bed_record_id)

        if not bed:
            raise ResourceNotFoundError(
                message="Bed not found.",
                meta={"bed_record_id": bed_record_id},
            )

        self.bed_repository.delete(bed_record_id)