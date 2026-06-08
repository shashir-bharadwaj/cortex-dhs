from typing import List

from app.domain.entities.icu_unit_master import ICUUnitMaster
from app.infrastructure.database.models.icu_unit_master import (
    ICUUnitMasterModel,
)


class ICUUnitMasterMapper:
    """
    Mapper responsible for converting ICUUnitMaster domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: ICUUnitMasterModel,
    ) -> ICUUnitMaster:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        return ICUUnitMaster(
            id=model.id,
            icu_name=model.icu_name,
            type=model.type,
            department=model.department,
            beds=model.beds,
            devices=model.devices,
            gateway=model.gateway,
            status=model.status,
        )

    @staticmethod
    def to_model(
        entity: ICUUnitMaster,
    ) -> ICUUnitMasterModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return ICUUnitMasterModel(
            id=entity.id,
            icu_name=entity.icu_name,
            type=entity.type,
            department=entity.department,
            beds=entity.beds,
            devices=entity.devices,
            gateway=entity.gateway,
            status=entity.status,
        )

    @staticmethod
    def to_domain_list(
        models: List[ICUUnitMasterModel],
    ) -> List[ICUUnitMaster]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            ICUUnitMasterMapper.to_domain(model)
            for model in models
        ]