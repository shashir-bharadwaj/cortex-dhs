from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.device_master_repository import DeviceMasterRepository


class AssignDeviceToBedUseCase:
    """
    Use case for mapping a registered device to a bed.

    Final relation:
    ICU -> Bed -> Device
    """

    def __init__(
        self,
        device_master_repository: DeviceMasterRepository,
        bed_repository: BedRepository,
    ):
        self.device_master_repository = device_master_repository
        self.bed_repository = bed_repository

    def execute(self, device_record_id: int, bed_id: int):
        if not self.device_master_repository.exists_by_id(device_record_id):
            raise ResourceNotFoundError(
                message="Device not found.",
                meta={"device_record_id": device_record_id},
            )

        if not self.bed_repository.exists_by_id(bed_id):
            raise ResourceNotFoundError(
                message="Bed not found.",
                meta={"bed_id": bed_id},
            )

        return self.device_master_repository.assign_bed(
            device_id=device_record_id,
            bed_id=bed_id,
        )