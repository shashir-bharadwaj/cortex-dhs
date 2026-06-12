from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.ventilator_setting import VentilatorSetting
from app.domain.repositories.ventilator_setting_repository import VentilatorSettingRepository
from app.infrastructure.database.mappers.ventilator_setting_mapper import VentilatorSettingMapper
from app.infrastructure.database.models.ventilator_setting import VentilatorSettingModel


class SQLAlchemyVentilatorSettingRepository(VentilatorSettingRepository):
    """
    SQLAlchemy implementation of VentilatorSettingRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, setting: VentilatorSetting) -> VentilatorSetting:
        model = VentilatorSettingMapper.to_model(setting)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return VentilatorSettingMapper.to_domain(model)

    def get_latest_by_patient_id(self, patient_id: int) -> Optional[VentilatorSetting]:
        model = (
            self.db.query(VentilatorSettingModel)
            .filter(VentilatorSettingModel.patient_id == patient_id)
            .order_by(VentilatorSettingModel.recorded_at.desc())
            .first()
        )
        return VentilatorSettingMapper.to_domain(model) if model else None

    def list_by_patient_id(self, patient_id: int) -> List[VentilatorSetting]:
        models = (
            self.db.query(VentilatorSettingModel)
            .filter(VentilatorSettingModel.patient_id == patient_id)
            .order_by(VentilatorSettingModel.recorded_at.desc())
            .all()
        )
        return VentilatorSettingMapper.to_domain_list(models)
