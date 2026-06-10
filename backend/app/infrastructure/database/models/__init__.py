"""
Import all SQLAlchemy models here so that SQLAlchemy
registers every model class before relationships are resolved.

This prevents mapper errors like:
- expression 'Patient' failed to locate a name
- expression 'VitalModel' failed to locate a name
"""

from app.infrastructure.database.models.icu_unit_master import ICUUnitMasterModel
from app.infrastructure.database.models.patient import PatientModel
from app.infrastructure.database.models.vital import VitalModel
from app.infrastructure.database.models.timeline import TimelineEventModel
from app.infrastructure.database.models.role import RoleModel
from app.infrastructure.database.models.user import UserModel
from app.infrastructure.database.models.device_type import DeviceType
from app.infrastructure.database.models.hospital import HospitalModel
from app.infrastructure.database.models.hospital_unit import HospitalUnitModel
from app.infrastructure.database.models.alarm import AlarmModel
from app.infrastructure.database.models.bed import BedMasterModel
from app.infrastructure.database.models.device_master import DeviceMasterModel
from app.infrastructure.database.models.permission import PermissionModel
from app.infrastructure.database.models.role_permission import RolePermissionModel
from app.infrastructure.database.models.latest_vital import LatestVitalModel
from app.infrastructure.database.models.patient_staff_assignment import (
    PatientStaffAssignmentModel,
)


__all__ = [
    "PatientModel",
    "VitalModel",
    "TimelineEventModel",
    "RoleModel",
    "UserModel",
    "HospitalModel",
    "HospitalUnitModel",
    "DeviceType",
    "AlarmModel",
    "ICUUnitMasterModel",
    "BedMasterModel",
    "DeviceMasterModel",
    "PermissionModel",
    "RolePermissionModel",
    "LatestVitalModel",
    "PatientStaffAssignmentModel"

]
# Add future models here too