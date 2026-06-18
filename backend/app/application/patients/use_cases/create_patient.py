import uuid
from datetime import datetime, timezone

from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository


class CreatePatientUseCase:
    """
    Use case for creating a patient.
    """

    def __init__(
        self,
        patient_repository: PatientRepository,
    ):
        self.patient_repository = patient_repository

    def execute(
        self,
        patient: Patient,
    ) -> Patient:
        """
        Persist a new patient admission, auto-generating identifiers
        (MRN / CR number) and defaulting the admission time to now when
        the caller did not supply them.
        """

        if patient.admission_time is None:
            patient.admission_time = datetime.now(timezone.utc)

        if not patient.mrn or not patient.cr_number:
            seq = self.patient_repository.count() + 1

            if not patient.mrn:
                # Continue the seed's MRN-1000xx numbering scheme.
                patient.mrn = f"MRN-{100000 + seq}"

            if not patient.cr_number:
                # Sequence for readability + uuid suffix so the unique
                # constraint holds even if rows were deleted.
                patient.cr_number = f"CR-{seq:03d}-{uuid.uuid4().hex[:6].upper()}"

        return self.patient_repository.create(patient)