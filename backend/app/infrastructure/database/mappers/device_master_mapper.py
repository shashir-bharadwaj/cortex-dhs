from typing import List

from app.domain.entities.device_master import DeviceMaster
from app.infrastructure.database.models.device_master import (
    DeviceMasterModel,
)


class DeviceMasterMapper:
    """
    Mapper responsible for converting DeviceMaster domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: DeviceMasterModel,
    ) -> DeviceMaster:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        return DeviceMaster(
            id=model.id,
            device_type=model.device_type,
            manufacturer=model.manufacturer,
            model=model.model,
            serial=model.serial,
            bed_id=model.bed_id,
            ip_address=model.ip_address,
            status=model.status,
        )

    @staticmethod
    def to_model(
        entity: DeviceMaster,
    ) -> DeviceMasterModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return DeviceMasterModel(
            id=entity.id,
            device_type=entity.device_type,
            manufacturer=entity.manufacturer,
            model=entity.model,
            serial=entity.serial,
            bed_id=entity.bed_id,
            ip_address=entity.ip_address,
            status=entity.status,
        )

    @staticmethod
    def to_domain_list(
        models: List[DeviceMasterModel],
    ) -> List[DeviceMaster]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            DeviceMasterMapper.to_domain(model)
            for model in models
        ]