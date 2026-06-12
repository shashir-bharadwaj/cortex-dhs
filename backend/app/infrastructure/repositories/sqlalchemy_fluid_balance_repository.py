from datetime import date, datetime, timezone
from typing import List

from sqlalchemy.orm import Session

from app.domain.entities.fluid_balance import FluidBalance
from app.domain.repositories.fluid_balance_repository import FluidBalanceRepository
from app.infrastructure.database.mappers.fluid_balance_mapper import FluidBalanceMapper
from app.infrastructure.database.models.fluid_balance import FluidBalanceModel


class SQLAlchemyFluidBalanceRepository(FluidBalanceRepository):
    """
    SQLAlchemy implementation of FluidBalanceRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, record: FluidBalance) -> FluidBalance:
        model = FluidBalanceMapper.to_model(record)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return FluidBalanceMapper.to_domain(model)

    def list_by_patient_id_and_date(
        self, patient_id: int, target_date: date
    ) -> List[FluidBalance]:
        day_start = datetime(
            target_date.year, target_date.month, target_date.day,
            tzinfo=timezone.utc,
        )
        day_end = datetime(
            target_date.year, target_date.month, target_date.day,
            23, 59, 59, tzinfo=timezone.utc,
        )
        models = (
            self.db.query(FluidBalanceModel)
            .filter(
                FluidBalanceModel.patient_id == patient_id,
                FluidBalanceModel.recorded_at >= day_start,
                FluidBalanceModel.recorded_at <= day_end,
            )
            .order_by(FluidBalanceModel.recorded_at.asc())
            .all()
        )
        return FluidBalanceMapper.to_domain_list(models)

    def list_by_patient_id(self, patient_id: int) -> List[FluidBalance]:
        models = (
            self.db.query(FluidBalanceModel)
            .filter(FluidBalanceModel.patient_id == patient_id)
            .order_by(FluidBalanceModel.recorded_at.desc())
            .all()
        )
        return FluidBalanceMapper.to_domain_list(models)
