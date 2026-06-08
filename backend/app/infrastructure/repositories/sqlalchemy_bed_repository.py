from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.bed import BedMaster
from app.domain.repositories.bed_repository import BedRepository
from app.infrastructure.database.mappers.bed_master_mapper import BedMapper
from app.infrastructure.database.models.bed import BedMasterModel


class SQLAlchemyBedRepository(BedRepository):
    """
    SQLAlchemy implementation of BedRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, bed: BedMaster) -> BedMaster:
        model = BedMapper.to_model(bed)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return BedMapper.to_domain(model)

    def list(self) -> List[BedMaster]:
        models = (
            self.db.query(BedMasterModel)
            .order_by(BedMasterModel.id.desc())
            .all()
        )

        return BedMapper.to_domain_list(models)

    def list_by_icu_unit_id(self, icu_unit_id: int) -> List[BedMaster]:
        models = (
            self.db.query(BedMasterModel)
            .filter(BedMasterModel.icu_unit_id == icu_unit_id)
            .order_by(BedMasterModel.id.desc())
            .all()
        )

        return BedMapper.to_domain_list(models)

    def by_id(self, id: int) -> Optional[BedMaster]:
        model = (
            self.db.query(BedMasterModel)
            .filter(BedMasterModel.id == id)
            .first()
        )

        if not model:
            return None

        return BedMapper.to_domain(model)

    def by_bed_id(self, bed_id: str) -> Optional[BedMaster]:
        model = (
            self.db.query(BedMasterModel)
            .filter(BedMasterModel.bed_id == bed_id)
            .first()
        )

        if not model:
            return None

        return BedMapper.to_domain(model)

    def get_by_bed_id(self, bed_id: str) -> Optional[BedMaster]:
        """
        Resolve BedMaster using external bed code from Edge SDK.

        Example:
        --------
        B1, B2, ICU-101
        """
        return self.by_bed_id(bed_id)

    def exists_by_id(self, id: int) -> bool:
        return (
            self.db.query(BedMasterModel.id)
            .filter(BedMasterModel.id == id)
            .first()
            is not None
        )

    def exists_by_bed_id(self, bed_id: str) -> bool:
        return (
            self.db.query(BedMasterModel.id)
            .filter(BedMasterModel.bed_id == bed_id)
            .first()
            is not None
        )

    def exists_by_bed_id_except_id(self, bed_id: str, id: int) -> bool:
        return (
            self.db.query(BedMasterModel.id)
            .filter(
                BedMasterModel.bed_id == bed_id,
                BedMasterModel.id != id,
            )
            .first()
            is not None
        )

    def update(self, bed: BedMaster) -> BedMaster:
        model = (
            self.db.query(BedMasterModel)
            .filter(BedMasterModel.id == bed.id)
            .first()
        )

        model.bed_id = bed.bed_id
        model.icu_unit_id = bed.icu_unit_id
        model.bed_type = bed.bed_type
        model.department = bed.department
        model.ward = bed.ward
        model.floor = bed.floor
        model.room = bed.room
        model.cleaning_status = bed.cleaning_status
        model.maintenance_status = bed.maintenance_status
        model.operational_status = bed.operational_status
        model.last_sanitized = bed.last_sanitized

        self.db.commit()
        self.db.refresh(model)

        return BedMapper.to_domain(model)

    def delete(self, id: int) -> None:
        model = (
            self.db.query(BedMasterModel)
            .filter(BedMasterModel.id == id)
            .first()
        )

        if model:
            self.db.delete(model)
            self.db.commit()