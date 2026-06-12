from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.medication_order import MedicationOrder
from app.domain.enums.medication import MedicationOrderType, MedicationStatus
from app.domain.repositories.medication_order_repository import MedicationOrderRepository
from app.infrastructure.database.mappers.medication_order_mapper import MedicationOrderMapper
from app.infrastructure.database.models.medication_order import MedicationOrderModel


class SQLAlchemyMedicationOrderRepository(MedicationOrderRepository):
    """
    SQLAlchemy implementation of MedicationOrderRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, order: MedicationOrder) -> MedicationOrder:
        model = MedicationOrderMapper.to_model(order)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return MedicationOrderMapper.to_domain(model)

    def list_by_patient_id(self, patient_id: int) -> List[MedicationOrder]:
        models = (
            self.db.query(MedicationOrderModel)
            .filter(MedicationOrderModel.patient_id == patient_id)
            .order_by(MedicationOrderModel.created_at.desc())
            .all()
        )
        return MedicationOrderMapper.to_domain_list(models)

    def list_active_infusions_by_patient_id(self, patient_id: int) -> List[MedicationOrder]:
        models = (
            self.db.query(MedicationOrderModel)
            .filter(
                MedicationOrderModel.patient_id == patient_id,
                MedicationOrderModel.order_type == MedicationOrderType.INFUSION.value,
                MedicationOrderModel.status == MedicationStatus.RUNNING.value,
            )
            .order_by(MedicationOrderModel.created_at.desc())
            .all()
        )
        return MedicationOrderMapper.to_domain_list(models)

    def by_id(self, order_id: int) -> Optional[MedicationOrder]:
        model = (
            self.db.query(MedicationOrderModel)
            .filter(MedicationOrderModel.id == order_id)
            .first()
        )
        return MedicationOrderMapper.to_domain(model) if model else None

    def update_status(self, order_id: int, status: str) -> Optional[MedicationOrder]:
        model = (
            self.db.query(MedicationOrderModel)
            .filter(MedicationOrderModel.id == order_id)
            .first()
        )
        if not model:
            return None
        model.status = status
        self.db.commit()
        self.db.refresh(model)
        return MedicationOrderMapper.to_domain(model)
