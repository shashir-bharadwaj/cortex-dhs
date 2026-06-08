# app/infrastructure/database/mappers/latest_vital_maper.py

from typing import List

from app.domain.entities.latest_vital import LatestVital
from app.infrastructure.database.models.latest_vital import (
    LatestVitalModel,
)


class LatestVitalMapper:
    """
    Mapper responsible for converting
    LatestVital domain entities and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: LatestVitalModel,
    ) -> LatestVital:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        return LatestVital(
            id=model.id,
            patient_id=model.patient_id,
            bed_id=model.bed_id,
            device_id=model.device_id,
            hr=model.hr,
            bp_sys=model.bp_sys,
            bp_dia=model.bp_dia,
            spo2=model.spo2,
            temp=model.temp,
            rr=model.rr,
            status=model.status,
            recorded_at=model.recorded_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(
        entity: LatestVital,
    ) -> LatestVitalModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return LatestVitalModel(
            id=entity.id,
            patient_id=entity.patient_id,
            bed_id=entity.bed_id,
            device_id=entity.device_id,
            hr=entity.hr,
            bp_sys=entity.bp_sys,
            bp_dia=entity.bp_dia,
            spo2=entity.spo2,
            temp=entity.temp,
            rr=entity.rr,
            status=entity.status,
            recorded_at=entity.recorded_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain_list(
        models: List[LatestVitalModel],
    ) -> List[LatestVital]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            LatestVitalMapper.to_domain(model)
            for model in models
        ]