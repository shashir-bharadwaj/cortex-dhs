from app.core.errors.exceptions import ConflictError
from app.domain.entities.icu_unit_master import ICUUnitMaster
from app.domain.repositories.icu_unit_master_repository import ICUUnitMasterRepository


class CreateICUUnitUseCase:
    """
    Use case for creating an ICU unit.
    """

    def __init__(self, icu_unit_repository: ICUUnitMasterRepository):
        self.icu_unit_repository = icu_unit_repository

    def execute(self, payload) -> ICUUnitMaster:
        if self.icu_unit_repository.exists_by_icu_name(payload.icu_name):
            raise ConflictError(
                message="ICU unit with this name already exists.",
                meta={"icu_name": payload.icu_name},
            )

        icu_unit = ICUUnitMaster(
            id=None,
            icu_name=payload.icu_name,
            type=payload.type,
            department=payload.department,
            beds=payload.beds,
            devices=payload.devices,
            gateway=payload.gateway,
            status=payload.status,
        )

        return self.icu_unit_repository.create(icu_unit)