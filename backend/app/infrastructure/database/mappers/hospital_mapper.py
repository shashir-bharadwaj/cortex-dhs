from typing import List

from app.domain.entities.hospital import (
    Hospital,
    HospitalUnit,
)
from app.infrastructure.database.models.hospital import (
    HospitalModel,
)
from app.infrastructure.database.models.hospital_unit import (
    HospitalUnitModel,
)


class HospitalMapper:
    """
    Mapper responsible for converting Hospital and HospitalUnit
    domain entities and SQLAlchemy models.
    """

    # ------------------------------------------------------------------
    # Hospital mappings
    # ------------------------------------------------------------------

    @staticmethod
    def to_hospital_domain(
        model: HospitalModel,
    ) -> Hospital:
        return Hospital(
            id=model.id,
            name=model.name,
            code=model.code,
            address=model.address,
            city=model.city,
            state=model.state,
            country=model.country,
            contact_number=model.contact_number,
            email=model.email,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_hospital_model(
        entity: Hospital,
    ) -> HospitalModel:
        return HospitalModel(
            id=entity.id,
            name=entity.name,
            code=entity.code,
            address=entity.address,
            city=entity.city,
            state=entity.state,
            country=entity.country,
            contact_number=entity.contact_number,
            email=entity.email,
        )

    @staticmethod
    def to_hospital_domain_list(
        models: List[HospitalModel],
    ) -> List[Hospital]:
        return [
            HospitalMapper.to_hospital_domain(model)
            for model in models
        ]

    # ------------------------------------------------------------------
    # Hospital unit mappings
    # ------------------------------------------------------------------

    @staticmethod
    def to_unit_domain(
        model: HospitalUnitModel,
    ) -> HospitalUnit:
        return HospitalUnit(
            id=model.id,
            hospital_id=model.hospital_id,
            name=model.name,
            code=model.code,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_unit_model(
        entity: HospitalUnit,
    ) -> HospitalUnitModel:
        return HospitalUnitModel(
            id=entity.id,
            hospital_id=entity.hospital_id,
            name=entity.name,
            code=entity.code,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_unit_domain_list(
        models: List[HospitalUnitModel],
    ) -> List[HospitalUnit]:
        return [
            HospitalMapper.to_unit_domain(model)
            for model in models
        ]