from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.ventilator_setting import VentilatorSetting


class VentilatorSettingRepository(ABC):
    """
    Domain repository contract for ventilator settings.
    """

    @abstractmethod
    def create(self, setting: VentilatorSetting) -> VentilatorSetting:
        pass

    @abstractmethod
    def get_latest_by_patient_id(self, patient_id: int) -> Optional[VentilatorSetting]:
        pass

    @abstractmethod
    def list_by_patient_id(self, patient_id: int) -> List[VentilatorSetting]:
        pass
