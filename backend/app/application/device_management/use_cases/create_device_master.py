from app.core.errors.exceptions import ConflictError, ResourceNotFoundError
from app.domain.entities.device_master import DeviceMaster
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.device_master_repository import DeviceMasterRepository


class CreateDeviceMasterUseCase:
    """
    Use case for registering a device.
    """

    def __init__(
        self,
        device_master_repository: DeviceMasterRepository,
        bed_repository: BedRepository,
    ):
        self.device_master_repository = device_master_repository
        self.bed_repository = bed_repository

    def execute(self, payload) -> DeviceMaster:
        if self.device_master_repository.exists_by_serial(payload.serial):
            raise ConflictError(
                message="Device with this serial already exists.",
                meta={"serial": payload.serial},
            )

        if payload.bed_id is not None and not self.bed_repository.exists_by_id(
            payload.bed_id
        ):
            raise ResourceNotFoundError(
                message="Bed not found.",
                meta={"bed_id": payload.bed_id},
            )

        device = DeviceMaster(
            id=None,
            device_type=payload.device_type,
            manufacturer=payload.manufacturer,
            model=payload.model,
            serial=payload.serial,
            bed_id=payload.bed_id,
            ip_address=payload.ip_address,
            status=payload.status,
        )

        return self.device_master_repository.create(device)