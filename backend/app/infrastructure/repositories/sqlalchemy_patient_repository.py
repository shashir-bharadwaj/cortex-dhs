from typing import List, Optional

from sqlalchemy.orm import Session, joinedload, selectinload

from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository
from app.infrastructure.database.mappers.patient_mapper import PatientMapper
from app.infrastructure.database.models.alarm import AlarmModel
from app.infrastructure.database.models.clinical_note import ClinicalNoteModel
from app.infrastructure.database.models.fluid_balance import FluidBalanceModel
from app.infrastructure.database.models.lab_result import LabResultModel
from app.infrastructure.database.models.latest_vital import LatestVitalModel
from app.infrastructure.database.models.medication_order import (
    MedicationOrderModel,
)
from app.infrastructure.database.models.patient import PatientModel
from app.infrastructure.database.models.patient_staff_assignment import (
    PatientStaffAssignmentModel,
)
from app.infrastructure.database.models.timeline import TimelineEventModel
from app.infrastructure.database.models.ventilator_setting import (
    VentilatorSettingModel,
)
from app.infrastructure.database.models.vital import VitalModel


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
        Fetch a patient by ID with related details.

        Collection relationships use selectinload to avoid large joined
        result sets when patient detail pages need tab-ready data.
        """
        patient_model = (
            self.db.query(PatientModel)
            .options(
                selectinload(PatientModel.vitals),
                selectinload(PatientModel.timeline),
                joinedload(PatientModel.bed),
                joinedload(PatientModel.hospital),
            )
            .filter(PatientModel.id == patient_id)
            .first()
        )

        if not patient_model:
            return None

        return PatientMapper.to_domain(patient_model)

    def list(
        self,
        limit: int | None = None,
        offset: int = 0,
    ) -> List[Patient]:
        """
        List patients ordered by latest admission first.

        Supports limit/offset pagination for scroll-based loading. The
        secondary sort on id keeps ordering deterministic across pages
        when admission times tie.
        """
        query = (
            self.db.query(PatientModel)
            .order_by(
                PatientModel.admission_time.desc(),
                PatientModel.id.asc(),
            )
        )

        if offset:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        return PatientMapper.to_domain_list(query.all())

    def count(self) -> int:
        """Total number of patient records."""
        return self.db.query(PatientModel).count()

    def delete(self, patient_id: int) -> bool:
        """
        Hard-delete a patient and all dependent clinical records.

        Children are removed first to satisfy foreign-key constraints.
        """
        patient_model = (
            self.db.query(PatientModel)
            .filter(PatientModel.id == patient_id)
            .first()
        )

        if not patient_model:
            return False

        for model in [
            PatientStaffAssignmentModel, AlarmModel, LatestVitalModel,
            VitalModel, TimelineEventModel, ClinicalNoteModel,
            VentilatorSettingModel, LabResultModel, FluidBalanceModel,
            MedicationOrderModel,
        ]:
            self.db.query(model).filter(
                model.patient_id == patient_id
            ).delete(synchronize_session=False)

        self.db.query(PatientModel).filter(
            PatientModel.id == patient_id
        ).delete(synchronize_session=False)

        self.db.commit()
        return True

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
        Resolve currently active patient assigned to a bed.

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