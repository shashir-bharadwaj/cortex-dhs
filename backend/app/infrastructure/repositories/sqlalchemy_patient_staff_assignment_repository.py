from datetime import datetime
from typing import List

from sqlalchemy.orm import Session, joinedload

from app.domain.entities.patient_staff_assignment import (
    PatientStaffAssignment,
)
from app.domain.repositories.patient_staff_assignment_repository import (
    PatientStaffAssignmentRepository,
)
from app.infrastructure.database.mappers.patient_staff_assignment_mapper import (
    PatientStaffAssignmentMapper,
)
from app.infrastructure.database.models.patient_staff_assignment import (
    PatientStaffAssignmentModel,
)
from app.infrastructure.database.models.user import UserModel


class SQLAlchemyPatientStaffAssignmentRepository(
    PatientStaffAssignmentRepository
):
    """
    SQLAlchemy implementation of PatientStaffAssignmentRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        assignment: PatientStaffAssignment,
    ) -> PatientStaffAssignment:
        """
        Persist a new staff assignment.
        """
        model = PatientStaffAssignmentMapper.to_model(assignment)

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return PatientStaffAssignmentMapper.to_domain(model)

    def list_active_by_patient_id(
        self,
        patient_id: int,
    ) -> List[PatientStaffAssignment]:
        """
        Return active staff assignments for a patient.
        """
        models = (
            self.db.query(PatientStaffAssignmentModel)
            .options(
                joinedload(
                    PatientStaffAssignmentModel.user
                ).joinedload(UserModel.role)
            )
            .filter(
                PatientStaffAssignmentModel.patient_id == patient_id,
                PatientStaffAssignmentModel.is_active.is_(True),
            )
            .all()
        )

        return PatientStaffAssignmentMapper.to_domain_list(models)

    def list_by_patient_id(
        self,
        patient_id: int,
    ) -> List[PatientStaffAssignment]:
        """
        Return assignment history for a patient.
        """
        models = (
            self.db.query(PatientStaffAssignmentModel)
            .options(
                joinedload(
                    PatientStaffAssignmentModel.user
                ).joinedload(UserModel.role)
            )
            .filter(PatientStaffAssignmentModel.patient_id == patient_id)
            .order_by(PatientStaffAssignmentModel.assigned_at.desc())
            .all()
        )

        return PatientStaffAssignmentMapper.to_domain_list(models)

    def end_assignment(
        self,
        assignment_id: int,
    ) -> PatientStaffAssignment:
        """
        End an active assignment.
        """
        model = (
            self.db.query(PatientStaffAssignmentModel)
            .filter(PatientStaffAssignmentModel.id == assignment_id)
            .first()
        )

        if not model:
            raise ValueError("Assignment not found")

        model.is_active = False
        model.ended_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(model)

        return PatientStaffAssignmentMapper.to_domain(model)