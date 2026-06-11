from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.icu_unit_master import ICUUnitMaster
from app.domain.repositories.icu_unit_master_repository import (
    ICUUnitMasterRepository,
)
from app.infrastructure.database.mappers.icu_unit_master_mapper import (
    ICUUnitMasterMapper,
)
from app.infrastructure.database.models.icu_unit_master import (
    ICUUnitMasterModel,
)


class SQLAlchemyICUUnitMasterRepository(ICUUnitMasterRepository):
    """
    SQLAlchemy implementation of ICUUnitMasterRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, icu_unit: ICUUnitMaster) -> ICUUnitMaster:
        model = ICUUnitMasterMapper.to_model(icu_unit)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return ICUUnitMasterMapper.to_domain(model)

    def list(self) -> List[ICUUnitMaster]:
        models = (
            self.db.query(ICUUnitMasterModel)
            .order_by(ICUUnitMasterModel.id.asc())
            .all()
        )

        return ICUUnitMasterMapper.to_domain_list(models)

    def by_id(self, icu_unit_id: int) -> Optional[ICUUnitMaster]:
        model = (
            self.db.query(ICUUnitMasterModel)
            .filter(ICUUnitMasterModel.id == icu_unit_id)
            .first()
        )

        if not model:
            return None

        return ICUUnitMasterMapper.to_domain(model)

    def by_icu_name(self, icu_name: str) -> Optional[ICUUnitMaster]:
        model = (
            self.db.query(ICUUnitMasterModel)
            .filter(ICUUnitMasterModel.icu_name == icu_name)
            .first()
        )

        if not model:
            return None

        return ICUUnitMasterMapper.to_domain(model)

    def exists_by_id(self, icu_unit_id: int) -> bool:
        return (
            self.db.query(ICUUnitMasterModel.id)
            .filter(ICUUnitMasterModel.id == icu_unit_id)
            .first()
            is not None
        )

    def exists_by_icu_name(self, icu_name: str) -> bool:
        return (
            self.db.query(ICUUnitMasterModel.id)
            .filter(ICUUnitMasterModel.icu_name == icu_name)
            .first()
            is not None
        )

    def exists_by_icu_name_except_id(
        self,
        icu_name: str,
        icu_unit_id: int,
    ) -> bool:
        return (
            self.db.query(ICUUnitMasterModel.id)
            .filter(
                ICUUnitMasterModel.icu_name == icu_name,
                ICUUnitMasterModel.id != icu_unit_id,
            )
            .first()
            is not None
        )

    def update(self, icu_unit: ICUUnitMaster) -> ICUUnitMaster:
        model = (
            self.db.query(ICUUnitMasterModel)
            .filter(ICUUnitMasterModel.id == icu_unit.id)
            .first()
        )

        model.icu_name = icu_unit.icu_name
        model.type = icu_unit.type
        model.department = icu_unit.department
        model.beds = icu_unit.beds
        model.devices = icu_unit.devices
        model.gateway = icu_unit.gateway
        model.status = icu_unit.status

        self.db.commit()
        self.db.refresh(model)

        return ICUUnitMasterMapper.to_domain(model)

    def delete(self, icu_unit_id: int) -> None:
        model = (
            self.db.query(ICUUnitMasterModel)
            .filter(ICUUnitMasterModel.id == icu_unit_id)
            .first()
        )

        if model:
            self.db.delete(model)
            self.db.commit()