from datetime import date, datetime, timezone

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.repositories.fluid_balance_repository import FluidBalanceRepository
from app.domain.repositories.patient_repository import PatientRepository


class GetDailyFluidBalanceUseCase:
    """
    Aggregate today's fluid intake and output for a patient.
    """

    def __init__(
        self,
        fluid_balance_repository: FluidBalanceRepository,
        patient_repository: PatientRepository,
    ):
        self.fluid_balance_repository = fluid_balance_repository
        self.patient_repository = patient_repository

    def execute(self, patient_id: int, target_date: date | None = None) -> dict:
        patient = self.patient_repository.by_id(patient_id)
        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        if target_date is None:
            target_date = datetime.now(timezone.utc).date()

        records = self.fluid_balance_repository.list_by_patient_id_and_date(
            patient_id, target_date
        )

        total_in = sum(r.in_ml or 0.0 for r in records)
        total_out = sum(r.out_ml or 0.0 for r in records)

        return {
            "patient_id": patient_id,
            "date": target_date.isoformat(),
            "in_ml": total_in,
            "out_ml": total_out,
            "balance_ml": total_in - total_out,
        }
