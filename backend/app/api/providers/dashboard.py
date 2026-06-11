from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider

from app.application.dashboard.use_cases.get_dashboard_overview import (
    GetDashboardOverviewUseCase,
)
from app.application.dashboard.use_cases.list_dashboard_units import (
    ListDashboardUnitsUseCase,
)

from app.domain.repositories.alarm_repository import (
    AlarmRepository,
)
from app.domain.repositories.bed_repository import (
    BedRepository,
)
from app.domain.repositories.device_master_repository import (
    DeviceMasterRepository,
)
from app.domain.repositories.icu_unit_master_repository import (
    ICUUnitMasterRepository,
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
        icu_unit_repository: ICUUnitMasterRepository = Depends(
            RepositoryProvider.get_icu_unit_repository
        ),
        bed_repository: BedRepository = Depends(
            RepositoryProvider.get_bed_repository
        ),
        patient_repository: PatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
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
        """
        Build dashboard overview aggregation use case.
        """
        return GetDashboardOverviewUseCase(
            icu_unit_repository=icu_unit_repository,
            bed_repository=bed_repository,
            patient_repository=patient_repository,
            latest_vital_repository=latest_vital_repository,
            alarm_repository=alarm_repository,
            device_repository=device_repository,
        )

    @staticmethod
    def get_list_dashboard_units_use_case(
        icu_unit_repository: ICUUnitMasterRepository = Depends(
            RepositoryProvider.get_icu_unit_repository
        ),
    ) -> ListDashboardUnitsUseCase:
        """
        Build dashboard unit listing use case.
        """
        return ListDashboardUnitsUseCase(
            icu_unit_repository=icu_unit_repository,
        )