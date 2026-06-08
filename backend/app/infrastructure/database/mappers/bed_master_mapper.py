from typing import List

from app.domain.entities.bed import BedMaster
from app.infrastructure.database.models.bed import BedMasterModel


class BedMapper:
    """
    Mapper responsible for converting BedMaster domain entities
    and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: BedMasterModel,
    ) -> BedMaster:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        return BedMaster(
            id=model.id,
            bed_id=model.bed_id,
            icu_unit_id=model.icu_unit_id,
            bed_type=model.bed_type,
            department=model.department,
            ward=model.ward,
            floor=model.floor,
            room=model.room,
            cleaning_status=model.cleaning_status,
            maintenance_status=model.maintenance_status,
            operational_status=model.operational_status,
            last_sanitized=model.last_sanitized,
        )

    @staticmethod
    def to_model(
        entity: BedMaster,
    ) -> BedMasterModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return BedMasterModel(
            id=entity.id,
            bed_id=entity.bed_id,
            icu_unit_id=entity.icu_unit_id,
            bed_type=entity.bed_type,
            department=entity.department,
            ward=entity.ward,
            floor=entity.floor,
            room=entity.room,
            cleaning_status=entity.cleaning_status,
            maintenance_status=entity.maintenance_status,
            operational_status=entity.operational_status,
            last_sanitized=entity.last_sanitized,
        )

    @staticmethod
    def to_domain_list(
        models: List[BedMasterModel],
    ) -> List[BedMaster]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            BedMapper.to_domain(model)
            for model in models
        ]