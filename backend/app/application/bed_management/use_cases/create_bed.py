from app.core.errors.exceptions import ConflictError, ResourceNotFoundError
from app.domain.entities.bed import BedMaster
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.icu_unit_master_repository import ICUUnitMasterRepository


class CreateBedUseCase:
    """
    Use case for creating a bed.
    """

    def __init__(
        self,
        bed_repository: BedRepository,
        icu_unit_repository: ICUUnitMasterRepository,
    ):
        self.bed_repository = bed_repository
        self.icu_unit_repository = icu_unit_repository

    def execute(self, payload) -> BedMaster:
        if self.bed_repository.exists_by_bed_id(payload.bed_id):
            raise ConflictError(
                message="Bed with this bed_id already exists.",
                meta={"bed_id": payload.bed_id},
            )

        if not self.icu_unit_repository.exists_by_id(payload.icu_unit_id):
            raise ResourceNotFoundError(
                message="ICU unit not found.",
                meta={"icu_unit_id": payload.icu_unit_id},
            )

        bed = BedMaster(
            id=None,
            bed_id=payload.bed_id,
            icu_unit_id=payload.icu_unit_id,
            bed_type=payload.bed_type,
            department=payload.department,
            ward=payload.ward,
            floor=payload.floor,
            room=payload.room,
            cleaning_status=payload.cleaning_status,
            maintenance_status=payload.maintenance_status,
            operational_status=payload.operational_status,
            last_sanitized=payload.last_sanitized,
        )

        return self.bed_repository.create(bed)