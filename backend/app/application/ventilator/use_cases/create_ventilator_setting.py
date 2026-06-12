from datetime import UTC, datetime

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.ventilator_setting import VentilatorSetting
from app.domain.repositories.patient_repository import PatientRepository
from app.domain.repositories.ventilator_setting_repository import VentilatorSettingRepository


class CreateVentilatorSettingUseCase:
    """
    Record ventilator parameters for a patient.
    """

    def __init__(
        self,
        ventilator_repository: VentilatorSettingRepository,
        patient_repository: PatientRepository,
    ):
        self.ventilator_repository = ventilator_repository
        self.patient_repository = patient_repository

    def execute(
        self,
        patient_id: int,
        mode: str | None,
        fio2: float | None,
        peep: float | None,
        set_rr: int | None,
        tidal_volume: float | None,
    ) -> VentilatorSetting:
        patient = self.patient_repository.by_id(patient_id)
        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        setting = VentilatorSetting(
            patient_id=patient_id,
            mode=mode,
            fio2=fio2,
            peep=peep,
            set_rr=set_rr,
            tidal_volume=tidal_volume,
            recorded_at=datetime.now(UTC),
        )

        return self.ventilator_repository.create(setting)
