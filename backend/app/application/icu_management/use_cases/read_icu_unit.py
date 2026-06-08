from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.icu_unit_master import ICUUnitMaster
from app.domain.repositories.icu_unit_master_repository import ICUUnitMasterRepository


class ReadICUUnitUseCase:
    """
    Use case for reading a single ICU unit.
    """

    def __init__(self, icu_unit_repository: ICUUnitMasterRepository):
        self.icu_unit_repository = icu_unit_repository

    def execute(self, icu_unit_id: int) -> ICUUnitMaster:
        icu_unit = self.icu_unit_repository.by_id(icu_unit_id)

        if not icu_unit:
            raise ResourceNotFoundError(
                message="ICU unit not found.",
                meta={"icu_unit_id": icu_unit_id},
            )

        return icu_unit