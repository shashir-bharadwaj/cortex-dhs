from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider
from app.application.dashboard.use_cases.get_dashboard_overview import (
    GetDashboardOverviewUseCase,
)
from app.domain.repositories.alarm_repository import AlarmRepository
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.device_master_repository import (
    DeviceMasterRepository,
)
from app.domain.repositories.hospital_repository import (
    HospitalRepository,
)
from app.domain.repositories.latest_vital_repository import (
    LatestVitalRepository,
)
from app.domain.repositories.patient_repository import (
    PatientRepository,
)


class DashboardProvider:
    """
    Provider for dashboard use cases.
    """

    @staticmethod
    def get_dashboard_overview_use_case(
        hospital_repository: HospitalRepository = Depends(
            RepositoryProvider.get_hospital_repository
        ),
        bed_repository: BedRepository = Depends(
            RepositoryProvider.get_bed_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),

        # Dashboard overview now reads live patient vitals
        # from latest_patient_vitals instead of historical
        # vitals aggregation queries.
        latest_vital_repository: LatestVitalRepository = Depends(
            RepositoryProvider.get_latest_vital_repository
        ),

        alarm_repository: AlarmRepository = Depends(
            RepositoryProvider.get_alarm_repository
        ),

        device_repository: DeviceMasterRepository = Depends(
            RepositoryProvider.get_device_repository
        ),
    ) -> GetDashboardOverviewUseCase:
        return GetDashboardOverviewUseCase(
            hospital_repository=hospital_repository,
            bed_repository=bed_repository,
            patient_repository=patient_repository,
            latest_vital_repository=latest_vital_repository,
            alarm_repository=alarm_repository,
            device_repository=device_repository,
        )