from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.patients.use_cases.create_patient import (
    CreatePatientUseCase,
)
from app.application.patients.use_cases.discharge_patient import (
    DischargePatientUseCase,
)
from app.application.patients.use_cases.get_patient import (
    GetPatientUseCase,
)
from app.application.patients.use_cases.get_patient_details import (
    GetPatientDetailsUseCase,
)
from app.application.patients.use_cases.list_patients import (
    ListPatientsUseCase,
)
from app.application.patients.use_cases.update_patient import (
    UpdatePatientUseCase,
)
from app.domain.repositories.alarm_repository import AlarmRepository
from app.domain.repositories.clinical_note_repository import (
    ClinicalNoteRepository,
)
from app.domain.repositories.device_master_repository import (
    DeviceMasterRepository,
)
from app.domain.repositories.latest_vital_repository import (
    LatestVitalRepository,
)
from app.domain.repositories.patient_repository import PatientRepository
from app.domain.repositories.patient_staff_assignment_repository import (
    PatientStaffAssignmentRepository,
)
from app.domain.repositories.vital_repository import VitalRepository


class PatientProvider:
    """
    Dependency wiring for patient-related use cases.
    """

    @staticmethod
    def get_create_patient_use_case(
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> CreatePatientUseCase:
        return CreatePatientUseCase(
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_list_patients_use_case(
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> ListPatientsUseCase:
        return ListPatientsUseCase(
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_get_patient_use_case(
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> GetPatientUseCase:
        return GetPatientUseCase(
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_update_patient_use_case(
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> UpdatePatientUseCase:
        return UpdatePatientUseCase(
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_discharge_patient_use_case(
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> DischargePatientUseCase:
        return DischargePatientUseCase(
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_patient_details_use_case(
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
        latest_vital_repository: LatestVitalRepository = Depends(
            RepositoryProvider.get_latest_vital_repository
        ),
        vital_repository: VitalRepository = Depends(
            RepositoryProvider.get_vital_repository
        ),
        device_repository: DeviceMasterRepository = Depends(
            RepositoryProvider.get_device_repository
        ),
        alarm_repository: AlarmRepository = Depends(
            RepositoryProvider.get_alarm_repository
        ),
        patient_staff_assignment_repository: PatientStaffAssignmentRepository = Depends(
            RepositoryProvider.get_patient_staff_assignment_repository
        ),
        clinical_note_repository: ClinicalNoteRepository = Depends(
            RepositoryProvider.get_clinical_note_repository
        ),
    ) -> GetPatientDetailsUseCase:
        """
        Build patient details aggregation use case.
        """
        return GetPatientDetailsUseCase(
            patient_repository=patient_repository,
            latest_vital_repository=latest_vital_repository,
            vital_repository=vital_repository,
            device_repository=device_repository,
            alarm_repository=alarm_repository,
            patient_staff_assignment_repository=(
                patient_staff_assignment_repository
            ),
            clinical_note_repository=clinical_note_repository,
        )