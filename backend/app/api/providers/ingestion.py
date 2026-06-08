from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.providers.db import DBProvider

from app.application.ingestion.use_cases.ingest_device_events import (
    IngestDeviceEventsUseCase,
)

from app.infrastructure.repositories.sqlalchemy_alarm_repository import (
    SQLAlchemyAlarmRepository,
)
from app.infrastructure.repositories.sqlalchemy_bed_repository import (
    SQLAlchemyBedRepository,
)
from app.infrastructure.repositories.sqlalchemy_latest_vital_repository import (
    SQLAlchemyLatestVitalRepository,
)
from app.infrastructure.repositories.sqlalchemy_patient_repository import (
    SQLAlchemyPatientRepository,
)
from app.infrastructure.repositories.sqlalchemy_vital_repository import (
    SQLAlchemyVitalRepository,
)


class IngestionProvider:
    """
    Provider responsible for constructing ingestion use cases.

    Responsibility:
    ---------------
    Centralize ingestion dependency wiring so endpoints
    remain lightweight and consistent with provider pattern.
    """

    @staticmethod
    def ingest_device_events_use_case(
        db: Session = Depends(
            DBProvider.get_db_session
        ),
    ) -> IngestDeviceEventsUseCase:
        """
        Provide ingestion use case.
        """
        return IngestDeviceEventsUseCase(
            bed_repository=SQLAlchemyBedRepository(db),
            patient_repository=SQLAlchemyPatientRepository(db),
            vital_repository=SQLAlchemyVitalRepository(db),
            latest_vital_repository=SQLAlchemyLatestVitalRepository(db),
            alarm_repository=SQLAlchemyAlarmRepository(db),
        )