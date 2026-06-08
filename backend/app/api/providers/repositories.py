from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.providers.db import DBProvider
from app.domain.repositories.latest_vital_repository import LatestVitalRepository
from app.infrastructure.repositories.sqlalchemy_alarm_repository import (
    SQLAlchemyAlarmRepository,
)
from app.infrastructure.repositories.sqlalchemy_bed_repository import SQLAlchemyBedRepository
from app.infrastructure.repositories.sqlalchemy_device_master_repository import SQLAlchemyDeviceMasterRepository
from app.infrastructure.repositories.sqlalchemy_hospital_repository import SQLAlchemyHospitalRepository
from app.infrastructure.repositories.sqlalchemy_latest_vital_repository import SQLAlchemyLatestVitalRepository
from app.infrastructure.repositories.sqlalchemy_patient_repository import (
    SQLAlchemyPatientRepository,
)
from app.infrastructure.repositories.sqlalchemy_permission_repository import (
    SQLAlchemyPermissionRepository,
)
from app.infrastructure.repositories.sqlalchemy_role_permission_repository import (
    SQLAlchemyRolePermissionRepository,
)
from app.infrastructure.repositories.sqlalchemy_role_repository import (
    SQLAlchemyRoleRepository,
)
from app.infrastructure.repositories.sqlalchemy_timeline_repository import (
    SQLAlchemyTimelineRepository,
)
from app.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.infrastructure.repositories.sqlalchemy_vital_repository import (
    SQLAlchemyVitalRepository,
)


class RepositoryProvider:
    """
    Provider class responsible for constructing repository instances.
    """

    @staticmethod
    def get_patient_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyPatientRepository:
        return SQLAlchemyPatientRepository(db)

    @staticmethod
    def get_vital_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyVitalRepository:
        return SQLAlchemyVitalRepository(db)

    @staticmethod
    def get_timeline_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyTimelineRepository:
        return SQLAlchemyTimelineRepository(db)

    @staticmethod
    def get_user_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(db)

    @staticmethod
    def get_role_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyRoleRepository:
        return SQLAlchemyRoleRepository(db)

    @staticmethod
    def get_permission_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyPermissionRepository:
        return SQLAlchemyPermissionRepository(db)

    @staticmethod
    def get_role_permission_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyRolePermissionRepository:
        return SQLAlchemyRolePermissionRepository(db)

    @staticmethod
    def get_alarm_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyAlarmRepository:
        return SQLAlchemyAlarmRepository(db)
    

    @staticmethod
    def get_hospital_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyHospitalRepository:
        return SQLAlchemyHospitalRepository(db)

    @staticmethod
    def get_bed_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyBedRepository:
        return SQLAlchemyBedRepository(db)

    @staticmethod
    def get_device_repository(
        db: Session = Depends(DBProvider.get_db_session),
    ) -> SQLAlchemyDeviceMasterRepository:
        return SQLAlchemyDeviceMasterRepository(db)
    
    @staticmethod
    def get_latest_vital_repository(
    db: Session = Depends(DBProvider.get_db_session),
    ) -> LatestVitalRepository:
        """
        Provide latest vital snapshot repository.
        """
        return SQLAlchemyLatestVitalRepository(db)