from app.core.errors.exceptions import ConflictError, ResourceNotFoundError
from app.domain.entities.device_master import DeviceMaster
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.device_master_repository import DeviceMasterRepository


class UpdateDeviceMasterUseCase:
    """
    Use case for updating a registered device.
    """

    def __init__(
        self,
        device_master_repository: DeviceMasterRepository,
        bed_repository: BedRepository,
    ):
        self.device_master_repository = device_master_repository
        self.bed_repository = bed_repository

    def execute(self, device_record_id: int, payload) -> DeviceMaster:
        existing = self.device_master_repository.by_id(device_record_id)

        if not existing:
            raise ResourceNotFoundError(
                message="Device not found.",
                meta={"device_record_id": device_record_id},
            )

        if self.device_master_repository.exists_by_serial_except_id(
            payload.serial,
            device_record_id,
        ):
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
            id=device_record_id,
            device_type=payload.device_type,
            manufacturer=payload.manufacturer,
            model=payload.model,
            serial=payload.serial,
            bed_id=payload.bed_id,
            ip_address=payload.ip_address,
            status=payload.status,
        )

        return self.device_master_repository.update(device)