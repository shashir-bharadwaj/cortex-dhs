from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.lab_result import LabResult
from app.domain.repositories.lab_result_repository import LabResultRepository
from app.infrastructure.database.mappers.lab_result_mapper import LabResultMapper
from app.infrastructure.database.models.lab_result import LabResultModel


class SQLAlchemyLabResultRepository(LabResultRepository):
    """
    SQLAlchemy implementation of LabResultRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, result: LabResult) -> LabResult:
        model = LabResultMapper.to_model(result)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return LabResultMapper.to_domain(model)

    def get_latest_by_patient_id(self, patient_id: int) -> Optional[LabResult]:
        model = (
            self.db.query(LabResultModel)
            .filter(LabResultModel.patient_id == patient_id)
            .order_by(LabResultModel.recorded_at.desc())
            .first()
        )
        return LabResultMapper.to_domain(model) if model else None

    def list_by_patient_id(self, patient_id: int) -> List[LabResult]:
        models = (
            self.db.query(LabResultModel)
            .filter(LabResultModel.patient_id == patient_id)
            .order_by(LabResultModel.recorded_at.desc())
            .all()
        )
        return LabResultMapper.to_domain_list(models)
