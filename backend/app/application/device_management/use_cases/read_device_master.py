from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.device_master import DeviceMaster
from app.domain.repositories.device_master_repository import DeviceMasterRepository


class ReadDeviceMasterUseCase:
    """
    Use case for reading a single registered device.
    """

    def __init__(self, device_master_repository: DeviceMasterRepository):
        self.device_master_repository = device_master_repository

    def execute(self, device_record_id: int) -> DeviceMaster:
        device = self.device_master_repository.by_id(device_record_id)

        if not device:
            raise ResourceNotFoundError(
                message="Device not found.",
                meta={"device_record_id": device_record_id},
            )

        return device