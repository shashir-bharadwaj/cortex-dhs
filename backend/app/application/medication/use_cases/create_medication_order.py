from datetime import UTC, datetime
from typing import Optional

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.medication_order import MedicationOrder
from app.domain.enums.medication import MedicationOrderType, MedicationStatus
from app.domain.repositories.medication_order_repository import MedicationOrderRepository
from app.domain.repositories.patient_repository import PatientRepository


class CreateMedicationOrderUseCase:
    """
    Create a medication order for an ICU patient.
    """

    def __init__(
        self,
        medication_order_repository: MedicationOrderRepository,
        patient_repository: PatientRepository,
    ):
        self.medication_order_repository = medication_order_repository
        self.patient_repository = patient_repository

    def execute(
        self,
        patient_id: int,
        drug_name: str,
        order_type: MedicationOrderType,
        dose: Optional[str],
        route: Optional[str],
        schedule: Optional[str],
        status: MedicationStatus,
        rate_ml_hr: Optional[float],
        remaining_vol_ml: Optional[float],
        est_end_time: Optional[datetime],
    ) -> MedicationOrder:
        patient = self.patient_repository.by_id(patient_id)
        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        now = datetime.now(UTC)
        order = MedicationOrder(
            patient_id=patient_id,
            drug_name=drug_name,
            order_type=order_type,
            dose=dose,
            route=route,
            schedule=schedule,
            status=status,
            rate_ml_hr=rate_ml_hr,
            remaining_vol_ml=remaining_vol_ml,
            est_end_time=est_end_time,
            created_at=now,
            updated_at=now,
        )

        return self.medication_order_repository.create(order)
