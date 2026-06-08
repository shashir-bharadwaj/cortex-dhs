from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.device_master_repository import DeviceMasterRepository


class DeleteDeviceMasterUseCase:
    """
    Use case for deleting a registered device.
    """

    def __init__(self, device_master_repository: DeviceMasterRepository):
        self.device_master_repository = device_master_repository

    def execute(self, device_record_id: int) -> None:
        existing = self.device_master_repository.by_id(device_record_id)

        if not existing:
            raise ResourceNotFoundError(
                message="Device not found.",
                meta={"device_record_id": device_record_id},
            )

        self.device_master_repository.delete(device_record_id)