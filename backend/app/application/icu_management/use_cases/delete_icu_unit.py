from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.icu_unit_master_repository import ICUUnitMasterRepository


class DeleteICUUnitUseCase:
    """
    Use case for deleting an ICU unit.
    """

    def __init__(self, icu_unit_repository: ICUUnitMasterRepository):
        self.icu_unit_repository = icu_unit_repository

    def execute(self, icu_unit_id: int) -> None:
        existing = self.icu_unit_repository.by_id(icu_unit_id)

        if not existing:
            raise ResourceNotFoundError(
                message="ICU unit not found.",
                meta={"icu_unit_id": icu_unit_id},
            )

        self.icu_unit_repository.delete(icu_unit_id)