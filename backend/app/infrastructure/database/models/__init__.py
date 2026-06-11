"""
Import all SQLAlchemy models here so that SQLAlchemy
registers every model class before relationships are resolved.

This prevents mapper errors like:
- expression 'Patient' failed to locate a name
- expression 'VitalModel' failed to locate a name
"""

from app.infrastructure.database.models.alarm import AlarmModel
from app.infrastructure.database.models.bed import BedMasterModel
from app.infrastructure.database.models.clinical_note import (
    ClinicalNoteModel,
)
from app.infrastructure.database.models.device_master import (
    DeviceMasterModel,
)
from app.infrastructure.database.models.device_type import DeviceType
from app.infrastructure.database.models.hospital import HospitalModel
from app.infrastructure.database.models.hospital_unit import (
    HospitalUnitModel,
)
from app.infrastructure.database.models.icu_unit_master import (
    ICUUnitMasterModel,
)
from app.infrastructure.database.models.latest_vital import (
    LatestVitalModel,
)
from app.infrastructure.database.models.patient import PatientModel
from app.infrastructure.database.models.patient_staff_assignment import (
    PatientStaffAssignmentModel,
)
from app.infrastructure.database.models.permission import (
    PermissionModel,
)
from app.infrastructure.database.models.role import RoleModel
from app.infrastructure.database.models.role_permission import (
    RolePermissionModel,
)
from app.infrastructure.database.models.timeline import (
    TimelineEventModel,
)
from app.infrastructure.database.models.user import UserModel
from app.infrastructure.database.models.vital import VitalModel


__all__ = [
    "AlarmModel",
    "BedMasterModel",
    "ClinicalNoteModel",
    "DeviceMasterModel",
    "DeviceType",
    "HospitalModel",
    "HospitalUnitModel",
    "ICUUnitMasterModel",
    "LatestVitalModel",
    "PatientModel",
    "PatientStaffAssignmentModel",
    "PermissionModel",
    "RoleModel",
    "RolePermissionModel",
    "TimelineEventModel",
    "UserModel",
    "VitalModel",
]

# Add future models here too