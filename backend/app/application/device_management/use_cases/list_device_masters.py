from typing import List

from app.domain.entities.device_master import DeviceMaster
from app.domain.repositories.device_master_repository import DeviceMasterRepository


class ListDeviceMastersUseCase:
    """
    Use case for listing registered devices.
    """

    def __init__(self, device_master_repository: DeviceMasterRepository):
        self.device_master_repository = device_master_repository

    def execute(self) -> List[DeviceMaster]:
        return self.device_master_repository.list()