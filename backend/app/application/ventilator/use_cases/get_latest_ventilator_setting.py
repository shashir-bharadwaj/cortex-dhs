from typing import Optional

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.ventilator_setting import VentilatorSetting
from app.domain.repositories.patient_repository import PatientRepository
from app.domain.repositories.ventilator_setting_repository import VentilatorSettingRepository


class GetLatestVentilatorSettingUseCase:
    """
    Return the most recent ventilator setting for a patient.
    """

    def __init__(
        self,
        ventilator_repository: VentilatorSettingRepository,
        patient_repository: PatientRepository,
    ):
        self.ventilator_repository = ventilator_repository
        self.patient_repository = patient_repository

    def execute(self, patient_id: int) -> Optional[VentilatorSetting]:
        patient = self.patient_repository.by_id(patient_id)
        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )
        return self.ventilator_repository.get_latest_by_patient_id(patient_id)
