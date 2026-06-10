from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.patient_staff_assignment import (
    PatientStaffAssignment,
)


class PatientStaffAssignmentRepository(ABC):
    """
    Contract for patient staff assignment persistence.

    Supports:
    - assigned nurse lookup
    - assigned doctor lookup
    - care team display
    - future shift handovers
    - assignment history
    """

    @abstractmethod
    def create(
        self,
        assignment: PatientStaffAssignment,
    ) -> PatientStaffAssignment:
        pass

    @abstractmethod
    def list_active_by_patient_id(
        self,
        patient_id: int,
    ) -> List[PatientStaffAssignment]:
        """
        Return active staff assignments for a patient.
        """
        pass

    @abstractmethod
    def list_by_patient_id(
        self,
        patient_id: int,
    ) -> List[PatientStaffAssignment]:
        """
        Return assignment history for a patient.
        """
        pass

    @abstractmethod
    def end_assignment(
        self,
        assignment_id: int,
    ) -> PatientStaffAssignment:
        """
        Mark an assignment as inactive.
        """
        pass