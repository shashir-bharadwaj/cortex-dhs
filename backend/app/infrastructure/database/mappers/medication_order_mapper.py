from typing import List

from app.domain.entities.medication_order import MedicationOrder
from app.domain.enums.medication import MedicationOrderType, MedicationStatus
from app.infrastructure.database.models.medication_order import MedicationOrderModel


class MedicationOrderMapper:
    """
    Mapper for MedicationOrder domain entity and SQLAlchemy model.
    """

    @staticmethod
    def to_domain(model: MedicationOrderModel) -> MedicationOrder:
        return MedicationOrder(
            id=model.id,
            patient_id=model.patient_id,
            drug_name=model.drug_name,
            order_type=MedicationOrderType(model.order_type),
            dose=model.dose,
            route=model.route,
            schedule=model.schedule,
            status=MedicationStatus(model.status),
            rate_ml_hr=model.rate_ml_hr,
            remaining_vol_ml=model.remaining_vol_ml,
            est_end_time=model.est_end_time,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: MedicationOrder) -> MedicationOrderModel:
        return MedicationOrderModel(
            id=entity.id,
            patient_id=entity.patient_id,
            drug_name=entity.drug_name,
            order_type=entity.order_type.value,
            dose=entity.dose,
            route=entity.route,
            schedule=entity.schedule,
            status=entity.status.value,
            rate_ml_hr=entity.rate_ml_hr,
            remaining_vol_ml=entity.remaining_vol_ml,
            est_end_time=entity.est_end_time,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain_list(models: List[MedicationOrderModel]) -> List[MedicationOrder]:
        return [MedicationOrderMapper.to_domain(m) for m in models]
