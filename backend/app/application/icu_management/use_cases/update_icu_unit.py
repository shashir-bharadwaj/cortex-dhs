from app.core.errors.exceptions import ConflictError, ResourceNotFoundError
from app.domain.entities.icu_unit_master import ICUUnitMaster
from app.domain.repositories.icu_unit_master_repository import ICUUnitMasterRepository


class UpdateICUUnitUseCase:
    """
    Use case for updating an ICU unit.
    """

    def __init__(self, icu_unit_repository: ICUUnitMasterRepository):
        self.icu_unit_repository = icu_unit_repository

    def execute(self, icu_unit_id: int, payload) -> ICUUnitMaster:
        existing = self.icu_unit_repository.by_id(icu_unit_id)

        if not existing:
            raise ResourceNotFoundError(
                message="ICU unit not found.",
                meta={"icu_unit_id": icu_unit_id},
            )

        if self.icu_unit_repository.exists_by_icu_name_except_id(
            payload.icu_name,
            icu_unit_id,
        ):
            raise ConflictError(
                message="ICU unit with this name already exists.",
                meta={"icu_name": payload.icu_name},
            )

        icu_unit = ICUUnitMaster(
            id=icu_unit_id,
            icu_name=payload.icu_name,
            type=payload.type,
            department=payload.department,
            beds=payload.beds,
            devices=payload.devices,
            gateway=payload.gateway,
            status=payload.status,
        )

        return self.icu_unit_repository.update(icu_unit)