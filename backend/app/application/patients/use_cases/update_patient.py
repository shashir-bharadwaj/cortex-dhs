from app.core.errors.exceptions import ResourceNotFoundError
from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository


class UpdatePatientUseCase:
    """
    Use case for updating a patient.
    """

    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    # Identifiers / lifecycle fields are preserved on edit, never nulled.
    _MERGE_FIELDS = (
        "name", "age", "gender", "bed_id", "diagnosis", "weight",
        "height", "blood_group", "doctor", "admission_time", "hospital_id",
    )

    def execute(self, patient_id: int, patient: Patient) -> Patient:
        existing = self.patient_repository.by_id(patient_id)

        if not existing:
            raise ResourceNotFoundError(
                message="Patient not found.",
                meta={"patient_id": patient_id},
            )

        # Partial merge: only overwrite fields the caller actually supplied,
        # so omitted columns (e.g. hospital_id, admission_time, history)
        # keep their existing values instead of being set to NULL.
        for field in self._MERGE_FIELDS:
            value = getattr(patient, field, None)
            if value is not None:
                setattr(existing, field, value)

        for field in ("history", "comorbidities"):
            value = getattr(patient, field, None)
            if value:
                setattr(existing, field, value)

        return self.patient_repository.update(existing)