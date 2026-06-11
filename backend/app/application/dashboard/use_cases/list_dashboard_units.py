from app.domain.repositories.icu_unit_master_repository import (
    ICUUnitMasterRepository,
)


class ListDashboardUnitsUseCase:
    """
    Use case for listing ICU units available to dashboard users.
    """

    def __init__(
        self,
        icu_unit_repository: ICUUnitMasterRepository,
    ):
        self.icu_unit_repository = icu_unit_repository

    def execute(self):
        return self.icu_unit_repository.list()