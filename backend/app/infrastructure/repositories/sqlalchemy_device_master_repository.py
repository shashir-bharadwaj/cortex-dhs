from collections import defaultdict
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.device_master import DeviceMaster
from app.domain.repositories.device_master_repository import DeviceMasterRepository
from app.infrastructure.database.mappers.device_master_mapper import (
    DeviceMasterMapper,
)
from app.infrastructure.database.models.device_master import DeviceMasterModel


class SQLAlchemyDeviceMasterRepository(DeviceMasterRepository):
    """
    SQLAlchemy implementation of DeviceMasterRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, device: DeviceMaster) -> DeviceMaster:
        model = DeviceMasterMapper.to_model(device)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return DeviceMasterMapper.to_domain(model)

    def list(self) -> List[DeviceMaster]:
        models = (
            self.db.query(DeviceMasterModel)
            .order_by(DeviceMasterModel.id.desc())
            .all()
        )

        return DeviceMasterMapper.to_domain_list(models)

    def list_by_bed_id(self, bed_id: int) -> List[DeviceMaster]:
        models = (
            self.db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.bed_id == bed_id)
            .order_by(DeviceMasterModel.id.desc())
            .all()
        )

        return DeviceMasterMapper.to_domain_list(models)

    def by_id(self, id: int) -> Optional[DeviceMaster]:
        model = (
            self.db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.id == id)
            .first()
        )

        if not model:
            return None

        return DeviceMasterMapper.to_domain(model)

    def by_serial(self, serial: str) -> Optional[DeviceMaster]:
        model = (
            self.db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.serial == serial)
            .first()
        )

        if not model:
            return None

        return DeviceMasterMapper.to_domain(model)

    def exists_by_id(self, id: int) -> bool:
        return (
            self.db.query(DeviceMasterModel.id)
            .filter(DeviceMasterModel.id == id)
            .first()
            is not None
        )

    def exists_by_serial(self, serial: str) -> bool:
        return (
            self.db.query(DeviceMasterModel.id)
            .filter(DeviceMasterModel.serial == serial)
            .first()
            is not None
        )

    def exists_by_serial_except_id(
        self,
        serial: str,
        id: int,
    ) -> bool:
        return (
            self.db.query(DeviceMasterModel.id)
            .filter(
                DeviceMasterModel.serial == serial,
                DeviceMasterModel.id != id,
            )
            .first()
            is not None
        )

    def update(self, device: DeviceMaster) -> DeviceMaster:
        model = (
            self.db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.id == device.id)
            .first()
        )

        model.device_type = device.device_type
        model.manufacturer = device.manufacturer
        model.model = device.model
        model.serial = device.serial
        model.bed_id = device.bed_id
        model.ip_address = device.ip_address
        model.status = device.status

        self.db.commit()
        self.db.refresh(model)

        return DeviceMasterMapper.to_domain(model)

    def assign_bed(
        self,
        device_id: int,
        bed_id: int,
    ) -> Optional[DeviceMaster]:
        model = (
            self.db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.id == device_id)
            .first()
        )

        if not model:
            return None

        model.bed_id = bed_id

        self.db.commit()
        self.db.refresh(model)

        return DeviceMasterMapper.to_domain(model)

    def unassign_bed(
        self,
        device_id: int,
    ) -> Optional[DeviceMaster]:
        model = (
            self.db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.id == device_id)
            .first()
        )

        if not model:
            return None

        model.bed_id = None

        self.db.commit()
        self.db.refresh(model)

        return DeviceMasterMapper.to_domain(model)

    def delete(self, id: int) -> None:
        model = (
            self.db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.id == id)
            .first()
        )

        if model:
            self.db.delete(model)
            self.db.commit()

    def list_by_bed_ids(
        self,
        bed_ids: List[int],
    ) -> Dict[int, List[str]]:
        """
        Return monitoring devices grouped by bed id.
        """
        if not bed_ids:
            return {}

        models = (
            self.db.query(DeviceMasterModel)
            .filter(DeviceMasterModel.bed_id.in_(bed_ids))
            .all()
        )

        grouped_devices: Dict[int, List[str]] = defaultdict(list)

        for model in models:
            grouped_devices[model.bed_id].append(model.device_type)

        return dict(grouped_devices)