from typing import List

from app.domain.entities.icu_unit_master import ICUUnitMaster
from app.domain.repositories.icu_unit_master_repository import ICUUnitMasterRepository


class ListICUUnitsUseCase:
    """
    Use case for listing ICU units.
    """

    def __init__(self, icu_unit_repository: ICUUnitMasterRepository):
        self.icu_unit_repository = icu_unit_repository

    def execute(self) -> List[ICUUnitMaster]:
        return self.icu_unit_repository.list()