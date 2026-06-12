from typing import List

from app.domain.entities.lab_result import LabResult
from app.infrastructure.database.models.lab_result import LabResultModel


class LabResultMapper:
    """
    Mapper for LabResult domain entity and SQLAlchemy model.
    """

    @staticmethod
    def to_domain(model: LabResultModel) -> LabResult:
        return LabResult(
            id=model.id,
            patient_id=model.patient_id,
            ph=model.ph,
            pao2=model.pao2,
            paco2=model.paco2,
            hco3=model.hco3,
            rbs=model.rbs,
            recorded_at=model.recorded_at,
        )

    @staticmethod
    def to_model(entity: LabResult) -> LabResultModel:
        return LabResultModel(
            id=entity.id,
            patient_id=entity.patient_id,
            ph=entity.ph,
            pao2=entity.pao2,
            paco2=entity.paco2,
            hco3=entity.hco3,
            rbs=entity.rbs,
            recorded_at=entity.recorded_at,
        )

    @staticmethod
    def to_domain_list(models: List[LabResultModel]) -> List[LabResult]:
        return [LabResultMapper.to_domain(m) for m in models]
