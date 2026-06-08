from fastapi import Depends

from app.api.providers.repositories import RepositoryProvider

from app.application.timeline.use_cases.create_timeline_event import (
    CreateTimelineEventUseCase,
)
from app.application.timeline.use_cases.list_patient_timeline import (
    ListPatientTimelineUseCase,
)

from app.infrastructure.repositories.sqlalchemy_patient_repository import (
    SQLAlchemyPatientRepository,
)
from app.infrastructure.repositories.sqlalchemy_timeline_repository import (
    SQLAlchemyTimelineRepository,
)


class TimelineProvider:
    """
    Provider class responsible for constructing
    Timeline-related application use cases.

    Why this exists:
    ----------------
    Keeps route files focused on HTTP concerns only, while all
    dependency wiring lives here in one predictable place.
    """

    @staticmethod
    def get_create_timeline_event_use_case(
        # Repository used to persist timeline entries
        timeline_repository: SQLAlchemyTimelineRepository = Depends(
            RepositoryProvider.get_timeline_repository
        ),
        # Repository used to validate patient existence before writing an event
        patient_repository: SQLAlchemyPatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> CreateTimelineEventUseCase:
        """
        Build the use case for creating a patient timeline event.

        Business rule:
        --------------
        A timeline event should only be created if the patient exists.
        """
        return CreateTimelineEventUseCase(
            timeline_repository=timeline_repository,
            patient_repository=patient_repository,
        )

    @staticmethod
    def get_list_patient_timeline_use_case(
        # Repository used to fetch timeline entries for a patient
        timeline_repository: SQLAlchemyTimelineRepository = Depends(
            RepositoryProvider.get_timeline_repository
        ),
        # Repository used to validate patient existence first
        patient_repository: SQLAlchemyPatientRepository = Depends(
            RepositoryProvider.get_patient_repository
        ),
    ) -> ListPatientTimelineUseCase:
        """
        Build the use case for listing a patient's timeline.

        Why patient repository is also needed:
        --------------------------------------
        We validate the patient exists before returning timeline data.
        This prevents returning misleading empty results for invalid IDs.
        """
        return ListPatientTimelineUseCase(
            timeline_repository=timeline_repository,
            patient_repository=patient_repository,
        )