from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.hospital import Hospital, HospitalUnit
from app.domain.repositories.hospital_repository import HospitalRepository
from app.infrastructure.database.mappers.hospital_mapper import HospitalMapper
from app.infrastructure.database.models.hospital import HospitalModel
from app.infrastructure.database.models.hospital_unit import HospitalUnitModel


class SQLAlchemyHospitalRepository(HospitalRepository):
    """
    SQLAlchemy implementation of HospitalRepository.

    Kept with the existing class/file name to avoid wider import churn.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_hospital(self, hospital: Hospital) -> Hospital:
        model = HospitalMapper.to_hospital_model(hospital)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return HospitalMapper.to_hospital_domain(model)

    def get_hospital(self, hospital_id: int) -> Optional[Hospital]:
        model = (
            self.db.query(HospitalModel)
            .filter(HospitalModel.id == hospital_id)
            .first()
        )

        if not model:
            return None

        return HospitalMapper.to_hospital_domain(model)

    def list_hospitals(self) -> List[Hospital]:
        models = (
            self.db.query(HospitalModel)
            .order_by(HospitalModel.id.desc())
            .all()
        )

        return HospitalMapper.to_hospital_domain_list(models)

    def create_unit(self, unit: HospitalUnit) -> HospitalUnit:
        model = HospitalMapper.to_unit_model(unit)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return HospitalMapper.to_unit_domain(model)

    def get_unit(self, unit_id: int) -> Optional[HospitalUnit]:
        model = (
            self.db.query(HospitalUnitModel)
            .filter(HospitalUnitModel.id == unit_id)
            .first()
        )

        if not model:
            return None

        return HospitalMapper.to_unit_domain(model)

    def list_units(
        self,
        hospital_id: Optional[int] = None,
    ) -> List[HospitalUnit]:
        query = self.db.query(HospitalUnitModel)

        if hospital_id is not None:
            query = query.filter(
                HospitalUnitModel.hospital_id == hospital_id
            )

        models = query.order_by(
            HospitalUnitModel.id.desc()
        ).all()

        return HospitalMapper.to_unit_domain_list(models)