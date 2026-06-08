from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.device_master_repository import DeviceMasterRepository


class UnassignDeviceFromBedUseCase:
    """
    Use case for removing device-bed mapping.
    """

    def __init__(self, device_master_repository: DeviceMasterRepository):
        self.device_master_repository = device_master_repository

    def execute(self, device_record_id: int):
        if not self.device_master_repository.exists_by_id(device_record_id):
            raise ResourceNotFoundError(
                message="Device not found.",
                meta={"device_record_id": device_record_id},
            )

        return self.device_master_repository.unassign_bed(device_record_id)