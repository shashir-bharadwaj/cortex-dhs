from datetime import UTC, datetime
from typing import Optional

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.fluid_balance import FluidBalance
from app.domain.repositories.fluid_balance_repository import FluidBalanceRepository
from app.domain.repositories.patient_repository import PatientRepository


class CreateFluidBalanceRecordUseCase:
    """
    Record a fluid intake or output entry for an ICU patient.
    """

    def __init__(
        self,
        fluid_balance_repository: FluidBalanceRepository,
        patient_repository: PatientRepository,
    ):
        self.fluid_balance_repository = fluid_balance_repository
        self.patient_repository = patient_repository

    def execute(
        self,
        patient_id: int,
        in_ml: Optional[float],
        out_ml: Optional[float],
        source: Optional[str],
    ) -> FluidBalance:
        patient = self.patient_repository.by_id(patient_id)
        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        record = FluidBalance(
            patient_id=patient_id,
            in_ml=in_ml or 0.0,
            out_ml=out_ml or 0.0,
            source=source,
            recorded_at=datetime.now(UTC),
        )

        return self.fluid_balance_repository.create(record)
