from datetime import UTC, datetime
from typing import Optional

from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.lab_result import LabResult
from app.domain.repositories.lab_result_repository import LabResultRepository
from app.domain.repositories.patient_repository import PatientRepository


class CreateLabResultUseCase:
    """
    Record lab result values for an ICU patient.
    """

    def __init__(
        self,
        lab_result_repository: LabResultRepository,
        patient_repository: PatientRepository,
    ):
        self.lab_result_repository = lab_result_repository
        self.patient_repository = patient_repository

    def execute(
        self,
        patient_id: int,
        ph: Optional[float],
        pao2: Optional[float],
        paco2: Optional[float],
        hco3: Optional[float],
        rbs: Optional[float],
    ) -> LabResult:
        patient = self.patient_repository.by_id(patient_id)
        if not patient:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        result = LabResult(
            patient_id=patient_id,
            ph=ph,
            pao2=pao2,
            paco2=paco2,
            hco3=hco3,
            rbs=rbs,
            recorded_at=datetime.now(UTC),
        )

        return self.lab_result_repository.create(result)
