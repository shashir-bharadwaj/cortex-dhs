from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository
from app.infrastructure.database.mappers.patient_mapper import PatientMapper
from app.infrastructure.database.models.patient import PatientModel


class SQLAlchemyPatientRepository(PatientRepository):
    """
    SQLAlchemy implementation of the PatientRepository contract.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, patient: Patient) -> Patient:
        """
        Persist a new patient record.
        """
        patient_model = PatientMapper.to_model(patient)

        self.db.add(patient_model)
        self.db.commit()
        self.db.refresh(patient_model)

        return PatientMapper.to_domain(patient_model)

    def by_id(self, patient_id: int) -> Optional[Patient]:
        """
        Fetch a patient by ID with related ICU details.
        """
        patient_model = (
            self.db.query(PatientModel)
            .options(
                joinedload(PatientModel.vitals),
                joinedload(PatientModel.timeline),
                joinedload(PatientModel.bed),
                joinedload(PatientModel.hospital),
            )
            .filter(PatientModel.id == patient_id)
            .first()
        )

        if not patient_model:
            return None

        return PatientMapper.to_domain(patient_model)

    def list(self) -> List[Patient]:
        """
        List all patients ordered by latest admission first.
        """
        patient_models = (
            self.db.query(PatientModel)
            .order_by(PatientModel.admission_time.desc())
            .all()
        )

        return PatientMapper.to_domain_list(patient_models)

    def update(self, patient: Patient) -> Patient:
        """
        Update an existing patient record.
        """
        patient_model = (
            self.db.query(PatientModel)
            .filter(PatientModel.id == patient.id)
            .first()
        )

        if not patient_model:
            raise ValueError("Patient not found")

        patient_model.name = patient.name
        patient_model.age = patient.age
        patient_model.gender = patient.gender
        patient_model.bed_id = patient.bed_id
        patient_model.diagnosis = patient.diagnosis
        patient_model.weight = patient.weight
        patient_model.height = patient.height
        patient_model.blood_group = patient.blood_group
        patient_model.doctor = patient.doctor
        patient_model.admission_time = patient.admission_time
        patient_model.hospital_id = patient.hospital_id
        patient_model.history = patient.history
        patient_model.comorbidities = patient.comorbidities
        patient_model.status = patient.status

        self.db.commit()
        self.db.refresh(patient_model)

        return PatientMapper.to_domain(patient_model)

    def discharge(self, patient_id: int) -> Optional[Patient]:
        """
        Mark a patient as discharged.
        """
        patient_model = (
            self.db.query(PatientModel)
            .filter(PatientModel.id == patient_id)
            .first()
        )

        if not patient_model:
            return None

        patient_model.status = "discharged"

        self.db.commit()
        self.db.refresh(patient_model)

        return PatientMapper.to_domain(patient_model)

    def get_by_id(self, patient_id: int) -> Optional[Patient]:
        """
        Compatibility alias for older use cases.
        """
        return self.by_id(patient_id)

    def list_all(self) -> List[Patient]:
        """
        Compatibility alias for older use cases.
        """
        return self.list()

    def list_active_by_bed_ids(
        self,
        bed_ids: List[int],
    ) -> List[Patient]:
        """
        Fetch active patients assigned to the given beds.
        """
        if not bed_ids:
            return []

        models = (
            self.db.query(PatientModel)
            .filter(
                PatientModel.bed_id.in_(bed_ids),
                PatientModel.status != "discharged",
            )
            .all()
        )

        return PatientMapper.to_domain_list(models)

    def get_active_by_bed_id(
        self,
        bed_id: int,
    ) -> Optional[Patient]:
        """
        Resolve currently active patient assigned to bed.

        Used by ingestion flow to map external device/bed events
        to the current Cortex patient.
        """
        model = (
            self.db.query(PatientModel)
            .filter(
                PatientModel.bed_id == bed_id,
                PatientModel.status != "discharged",
            )
            .order_by(PatientModel.id.desc())
            .first()
        )

        if not model:
            return None

        return PatientMapper.to_domain(model)