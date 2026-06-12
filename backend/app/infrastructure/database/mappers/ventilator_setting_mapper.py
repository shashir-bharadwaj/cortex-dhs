from typing import List

from app.domain.entities.ventilator_setting import VentilatorSetting
from app.infrastructure.database.models.ventilator_setting import VentilatorSettingModel


class VentilatorSettingMapper:
    """
    Mapper for VentilatorSetting domain entity and SQLAlchemy model.
    """

    @staticmethod
    def to_domain(model: VentilatorSettingModel) -> VentilatorSetting:
        return VentilatorSetting(
            id=model.id,
            patient_id=model.patient_id,
            mode=model.mode,
            fio2=model.fio2,
            peep=model.peep,
            set_rr=model.set_rr,
            tidal_volume=model.tidal_volume,
            recorded_at=model.recorded_at,
        )

    @staticmethod
    def to_model(entity: VentilatorSetting) -> VentilatorSettingModel:
        return VentilatorSettingModel(
            id=entity.id,
            patient_id=entity.patient_id,
            mode=entity.mode,
            fio2=entity.fio2,
            peep=entity.peep,
            set_rr=entity.set_rr,
            tidal_volume=entity.tidal_volume,
            recorded_at=entity.recorded_at,
        )

    @staticmethod
    def to_domain_list(models: List[VentilatorSettingModel]) -> List[VentilatorSetting]:
        return [VentilatorSettingMapper.to_domain(m) for m in models]
