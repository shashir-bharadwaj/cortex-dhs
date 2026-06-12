from typing import List

from app.domain.entities.fluid_balance import FluidBalance
from app.infrastructure.database.models.fluid_balance import FluidBalanceModel


class FluidBalanceMapper:
    """
    Mapper for FluidBalance domain entity and SQLAlchemy model.
    """

    @staticmethod
    def to_domain(model: FluidBalanceModel) -> FluidBalance:
        return FluidBalance(
            id=model.id,
            patient_id=model.patient_id,
            in_ml=model.in_ml,
            out_ml=model.out_ml,
            source=model.source,
            recorded_at=model.recorded_at,
        )

    @staticmethod
    def to_model(entity: FluidBalance) -> FluidBalanceModel:
        return FluidBalanceModel(
            id=entity.id,
            patient_id=entity.patient_id,
            in_ml=entity.in_ml,
            out_ml=entity.out_ml,
            source=entity.source,
            recorded_at=entity.recorded_at,
        )

    @staticmethod
    def to_domain_list(models: List[FluidBalanceModel]) -> List[FluidBalance]:
        return [FluidBalanceMapper.to_domain(m) for m in models]
