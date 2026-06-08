from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.providers.db import DBProvider
from app.application.device_management.use_cases.assign_device_to_bed import (
    AssignDeviceToBedUseCase,
)
from app.application.device_management.use_cases.create_device_master import (
    CreateDeviceMasterUseCase,
)
from app.application.device_management.use_cases.delete_device_master import (
    DeleteDeviceMasterUseCase,
)
from app.application.device_management.use_cases.list_device_masters import (
    ListDeviceMastersUseCase,
)
from app.application.device_management.use_cases.list_devices_by_bed import (
    ListDevicesByBedUseCase,
)
from app.application.device_management.use_cases.read_device_master import (
    ReadDeviceMasterUseCase,
)
from app.application.device_management.use_cases.unassign_device_from_bed import (
    UnassignDeviceFromBedUseCase,
)
from app.application.device_management.use_cases.update_device_master import (
    UpdateDeviceMasterUseCase,
)
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.device_master_repository import (
    DeviceMasterRepository,
)
from app.infrastructure.repositories.sqlalchemy_bed_repository import (
    SQLAlchemyBedRepository,
)
from app.infrastructure.repositories.sqlalchemy_device_master_repository import (
    SQLAlchemyDeviceMasterRepository,
)


class DeviceManagementProvider:
    """
    Provider for device management dependencies.

    Provider layer wires infrastructure implementations
    to domain repository abstractions.
    """

    @staticmethod
    def device_master_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> DeviceMasterRepository:
        return SQLAlchemyDeviceMasterRepository(db)

    @staticmethod
    def bed_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> BedRepository:
        return SQLAlchemyBedRepository(db)

    @staticmethod
    def create_device_master_use_case(
        device_repository: DeviceMasterRepository = Depends(
            device_master_repository
        ),
        bed_repository: BedRepository = Depends(bed_repository),
    ) -> CreateDeviceMasterUseCase:
        return CreateDeviceMasterUseCase(
            device_master_repository=device_repository,
            bed_repository=bed_repository,
        )

    @staticmethod
    def list_device_masters_use_case(
        repository: DeviceMasterRepository = Depends(
            device_master_repository
        ),
    ) -> ListDeviceMastersUseCase:
        return ListDeviceMastersUseCase(repository)

    @staticmethod
    def read_device_master_use_case(
        repository: DeviceMasterRepository = Depends(
            device_master_repository
        ),
    ) -> ReadDeviceMasterUseCase:
        return ReadDeviceMasterUseCase(repository)

    @staticmethod
    def update_device_master_use_case(
        device_repository: DeviceMasterRepository = Depends(
            device_master_repository
        ),
        bed_repository: BedRepository = Depends(bed_repository),
    ) -> UpdateDeviceMasterUseCase:
        return UpdateDeviceMasterUseCase(
            device_master_repository=device_repository,
            bed_repository=bed_repository,
        )

    @staticmethod
    def delete_device_master_use_case(
        repository: DeviceMasterRepository = Depends(
            device_master_repository
        ),
    ) -> DeleteDeviceMasterUseCase:
        return DeleteDeviceMasterUseCase(repository)

    @staticmethod
    def assign_device_to_bed_use_case(
        device_repository: DeviceMasterRepository = Depends(
            device_master_repository
        ),
        bed_repository: BedRepository = Depends(bed_repository),
    ) -> AssignDeviceToBedUseCase:
        return AssignDeviceToBedUseCase(
            device_master_repository=device_repository,
            bed_repository=bed_repository,
        )

    @staticmethod
    def unassign_device_from_bed_use_case(
        repository: DeviceMasterRepository = Depends(
            device_master_repository
        ),
    ) -> UnassignDeviceFromBedUseCase:
        return UnassignDeviceFromBedUseCase(repository)

    @staticmethod
    def list_devices_by_bed_use_case(
        device_repository: DeviceMasterRepository = Depends(
            device_master_repository
        ),
        bed_repository: BedRepository = Depends(bed_repository),
    ) -> ListDevicesByBedUseCase:
        return ListDevicesByBedUseCase(
            device_master_repository=device_repository,
            bed_repository=bed_repository,
        )