from typing import List

from app.domain.entities.patient_staff_assignment import (
    PatientStaffAssignment,
)
from app.infrastructure.database.models.patient_staff_assignment import (
    PatientStaffAssignmentModel,
)


class PatientStaffAssignmentMapper:
    """
    Mapper responsible for converting PatientStaffAssignment
    domain entities and SQLAlchemy models.
    """

    @staticmethod
    def to_domain(
        model: PatientStaffAssignmentModel,
    ) -> PatientStaffAssignment:
        """
        Convert SQLAlchemy model -> domain entity.
        """

        staff_name = None
        staff_role = None

        if getattr(model, "user", None):
            staff_name = (
                f"{model.user.first_name} "
                f"{model.user.last_name}"
            ).strip()

            if getattr(model.user, "role", None):
                staff_role = model.user.role.name

        return PatientStaffAssignment(
            id=model.id,
            patient_id=model.patient_id,
            user_id=model.user_id,
            assignment_type=model.assignment_type,
            assigned_at=model.assigned_at,
            ended_at=model.ended_at,
            is_active=model.is_active,
            staff_name=staff_name,
            staff_role=staff_role,
        )

    @staticmethod
    def to_model(
        entity: PatientStaffAssignment,
    ) -> PatientStaffAssignmentModel:
        """
        Convert domain entity -> SQLAlchemy model.
        """

        return PatientStaffAssignmentModel(
            id=entity.id,
            patient_id=entity.patient_id,
            user_id=entity.user_id,
            assignment_type=entity.assignment_type,
            assigned_at=entity.assigned_at,
            ended_at=entity.ended_at,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_domain_list(
        models: List[PatientStaffAssignmentModel],
    ) -> List[PatientStaffAssignment]:
        """
        Convert SQLAlchemy model list -> domain entity list.
        """

        return [
            PatientStaffAssignmentMapper.to_domain(model)
            for model in models
        ]