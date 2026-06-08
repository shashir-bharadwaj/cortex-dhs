from app.core.errors.exceptions import ConflictError, ResourceNotFoundError
from app.domain.entities.bed import BedMaster
from app.domain.repositories.bed_repository import BedRepository
from app.domain.repositories.icu_unit_master_repository import ICUUnitMasterRepository


class UpdateBedUseCase:
    """
    Use case for updating a bed.
    """

    def __init__(
        self,
        bed_repository: BedRepository,
        icu_unit_repository: ICUUnitMasterRepository,
    ):
        self.bed_repository = bed_repository
        self.icu_unit_repository = icu_unit_repository

    def execute(self, bed_record_id: int, payload) -> BedMaster:
        existing = self.bed_repository.by_id(bed_record_id)

        if not existing:
            raise ResourceNotFoundError(
                message="Bed not found.",
                meta={"bed_record_id": bed_record_id},
            )

        if self.bed_repository.exists_by_bed_id_except_id(
            payload.bed_id,
            bed_record_id,
        ):
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
            id=bed_record_id,
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

        return self.bed_repository.update(bed)