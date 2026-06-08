from typing import List

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.device_master import DeviceMaster
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.device_master_repository import DeviceMasterRepository


class ListDevicesByBedUseCase:
    """
    Use case for listing devices mapped to a bed.
    """

    def __init__(
        self,
        device_master_repository: DeviceMasterRepository,
        bed_repository: BedRepository,
    ):
        self.device_master_repository = device_master_repository
        self.bed_repository = bed_repository

    def execute(self, bed_id: int) -> List[DeviceMaster]:
        if not self.bed_repository.exists_by_id(bed_id):
            raise ResourceNotFoundError(
                message="Bed not found.",
                meta={"bed_id": bed_id},
            )

        return self.device_master_repository.list_by_bed_id(bed_id)