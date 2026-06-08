from typing import List

from app.domain.entities.vital import Vital
from app.infrastructure.database.models.vital import VitalModel


class VitalMapper:
    """
    Mapper responsible for converting
    Vital domain entities and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: VitalModel,
    ) -> Vital:
        """
        Convert SQLAlchemy model -> domain entity.
        """
        return Vital(
            id=model.id,
            patient_id=model.patient_id,
            hr=model.hr,
            bp_sys=model.bp_sys,
            bp_dia=model.bp_dia,
            spo2=model.spo2,
            temp=model.temp,
            rr=model.rr,
            recorded_at=model.recorded_at,
        )

    @staticmethod
    def to_model(
        entity: Vital,
    ) -> VitalModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """
        return VitalModel(
            id=entity.id,
            patient_id=entity.patient_id,
            hr=entity.hr,
            bp_sys=entity.bp_sys,
            bp_dia=entity.bp_dia,
            spo2=entity.spo2,
            temp=entity.temp,
            rr=entity.rr,
            recorded_at=entity.recorded_at,
        )

    @staticmethod
    def to_domain_list(
        models: List[VitalModel],
    ) -> List[Vital]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """
        return [
            VitalMapper.to_domain(model)
            for model in models
        ]