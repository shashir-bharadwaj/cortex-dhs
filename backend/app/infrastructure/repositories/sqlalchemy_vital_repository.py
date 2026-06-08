from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.domain.entities.vital import Vital
from app.domain.repositories.vital_repository import VitalRepository
from app.infrastructure.database.models.vital import VitalModel
from app.infrastructure.database.mappers.vital_mapper import (
    VitalMapper,
)


class SQLAlchemyVitalRepository(VitalRepository):
    """
    SQLAlchemy implementation of the VitalRepository contract.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, vital: Vital) -> Vital:
        """
        Persist a new vital record.
        """
        vital_model = VitalMapper.to_model(vital)

        self.db.add(vital_model)
        self.db.commit()
        self.db.refresh(vital_model)

        return VitalMapper.to_domain(vital_model)

    def get_by_id(self, vital_id: int) -> Optional[Vital]:
        """
        Fetch a vital record by ID.
        """
        vital_model = (
            self.db.query(VitalModel)
            .filter(VitalModel.id == vital_id)
            .first()
        )

        if not vital_model:
            return None

        return VitalMapper.to_domain(vital_model)

    def list_by_patient_id(self, patient_id: int) -> List[Vital]:
        """
        Return all vital records for a patient ordered by newest first.
        """
        vital_models = (
            self.db.query(VitalModel)
            .filter(VitalModel.patient_id == patient_id)
            .order_by(VitalModel.recorded_at.desc())
            .all()
        )

        return VitalMapper.to_domain_list(vital_models)

    def list_latest_by_patient_id(
        self,
        patient_id: int,
        limit: int = 20,
    ) -> List[Vital]:
        """
        Return only the latest vital records for a patient.
        Useful for dashboards and charts.
        """
        vital_models = (
            self.db.query(VitalModel)
            .filter(VitalModel.patient_id == patient_id)
            .order_by(VitalModel.recorded_at.desc())
            .limit(limit)
            .all()
        )

        return VitalMapper.to_domain_list(vital_models)

    def list_latest_for_patients(
        self,
        patient_ids: list[int],
    ) -> dict[int, Vital]:
        """
        Fetch latest vitals grouped by patient id.
        """
        if not patient_ids:
            return {}

        models = (
            self.db.query(VitalModel)
            .filter(VitalModel.patient_id.in_(patient_ids))
            .order_by(
                VitalModel.patient_id,
                desc(VitalModel.recorded_at),
            )
            .all()
        )

        latest_vitals: dict[int, Vital] = {}

        for model in models:
            if model.patient_id not in latest_vitals:
                latest_vitals[model.patient_id] = VitalMapper.to_domain(model)

        return latest_vitals

    def create_from_ingestion(
        self,
        data: dict,
    ) -> Vital:
        """
        Persist ingestion-generated Vital row.
        """
        vital_model = VitalModel(
            patient_id=data["patient_id"],
            hr=data.get("hr"),
            bp_sys=data.get("bp_sys"),
            bp_dia=data.get("bp_dia"),
            spo2=data.get("spo2"),
            temp=data.get("temp"),
            rr=data.get("rr"),
            recorded_at=data["recorded_at"],
        )

        self.db.add(vital_model)
        self.db.commit()
        self.db.refresh(vital_model)

        return VitalMapper.to_domain(vital_model)