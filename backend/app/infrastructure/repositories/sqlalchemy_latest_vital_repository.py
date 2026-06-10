# app/infrastructure/database/repositories/sqlalchemy_latest_vital_repository.py

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.latest_vital import LatestVital
from app.domain.repositories.latest_vital_repository import (
    LatestVitalRepository,
)
from app.infrastructure.database.mappers.latest_vital_mapper import (
    LatestVitalMapper,
)
from app.infrastructure.database.models.latest_vital import (
    LatestVitalModel,
)


class SQLAlchemyLatestVitalRepository(LatestVitalRepository):
    """
    SQLAlchemy implementation of the LatestVitalRepository contract.

    This repository maintains one latest vital snapshot per patient.
    """

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, latest_vital: LatestVital) -> LatestVital:
        """
        Create or update latest vital snapshot for a patient.
        """
        existing_model = (
            self.db.query(LatestVitalModel)
            .filter(LatestVitalModel.patient_id == latest_vital.patient_id)
            .first()
        )

        if existing_model:
            existing_model.bed_id = latest_vital.bed_id
            existing_model.device_id = latest_vital.device_id
            existing_model.hr = latest_vital.hr
            existing_model.bp_sys = latest_vital.bp_sys
            existing_model.bp_dia = latest_vital.bp_dia
            existing_model.spo2 = latest_vital.spo2
            existing_model.temp = latest_vital.temp
            existing_model.rr = latest_vital.rr
            existing_model.status = latest_vital.status
            existing_model.recorded_at = latest_vital.recorded_at
            existing_model.updated_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(existing_model)

            return LatestVitalMapper.to_domain(existing_model)

        latest_vital_model = LatestVitalMapper.to_model(latest_vital)

        self.db.add(latest_vital_model)
        self.db.commit()
        self.db.refresh(latest_vital_model)

        return LatestVitalMapper.to_domain(latest_vital_model)

    def get_by_patient_id(
        self,
        patient_id: int,
    ) -> Optional[LatestVital]:
        """
        Fetch latest vital snapshot for a patient.
        """
        latest_vital_model = (
            self.db.query(LatestVitalModel)
            .filter(LatestVitalModel.patient_id == patient_id)
            .first()
        )

        if not latest_vital_model:
            return None

        return LatestVitalMapper.to_domain(latest_vital_model)

    def list_by_patient_ids(
        self,
        patient_ids: List[int],
    ) -> dict[int, LatestVital]:
        """
        Fetch latest vital snapshots for multiple patients.
        """
        if not patient_ids:
            return {}

        latest_vital_models = (
            self.db.query(LatestVitalModel)
            .filter(LatestVitalModel.patient_id.in_(patient_ids))
            .all()
        )

        latest_vitals: dict[int, LatestVital] = {}

        for model in latest_vital_models:
            latest_vitals[model.patient_id] = LatestVitalMapper.to_domain(
                model
            )

        return latest_vitals

    def list_by_bed_ids(
        self,
        bed_ids: List[int],
    ) -> List[LatestVital]:
        """
        Fetch latest vital snapshots for multiple beds.
        """
        if not bed_ids:
            return []

        latest_vital_models = (
            self.db.query(LatestVitalModel)
            .filter(LatestVitalModel.bed_id.in_(bed_ids))
            .all()
        )

        return LatestVitalMapper.to_domain_list(latest_vital_models)