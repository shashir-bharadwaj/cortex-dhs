from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.handover.use_cases.get_shift_summary import GetShiftSummaryUseCase
from app.infrastructure.repositories.sqlalchemy_alarm_repository import SQLAlchemyAlarmRepository
from app.infrastructure.repositories.sqlalchemy_clinical_note_repository import SQLAlchemyClinicalNoteRepository
from app.infrastructure.repositories.sqlalchemy_latest_vital_repository import SQLAlchemyLatestVitalRepository
from app.infrastructure.repositories.sqlalchemy_nurse_task_repository import SQLAlchemyNurseTaskRepository
from app.infrastructure.repositories.sqlalchemy_patient_repository import SQLAlchemyPatientRepository
from app.infrastructure.repositories.sqlalchemy_ventilator_setting_repository import SQLAlchemyVentilatorSettingRepository


class HandoverProvider:

    @staticmethod
    def get_shift_summary_use_case(
        patient_repository: SQLAlchemyPatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
        latest_vital_repository: SQLAlchemyLatestVitalRepository = Depends(
            RepositoryProvider.get_latest_vital_repository
        ),
        alarm_repository: SQLAlchemyAlarmRepository = Depends(
            RepositoryProvider.get_alarm_repository
        ),
        nurse_task_repository: SQLAlchemyNurseTaskRepository = Depends(
            RepositoryProvider.get_nurse_task_repository
        ),
        clinical_note_repository: SQLAlchemyClinicalNoteRepository = Depends(
            RepositoryProvider.get_clinical_note_repository
        ),
        ventilator_setting_repository: SQLAlchemyVentilatorSettingRepository = Depends(
            RepositoryProvider.get_ventilator_setting_repository
        ),
    ) -> GetShiftSummaryUseCase:
        return GetShiftSummaryUseCase(
            patient_repository=patient_repository,
            latest_vital_repository=latest_vital_repository,
            alarm_repository=alarm_repository,
            nurse_task_repository=nurse_task_repository,
            clinical_note_repository=clinical_note_repository,
            ventilator_setting_repository=ventilator_setting_repository,
        )
