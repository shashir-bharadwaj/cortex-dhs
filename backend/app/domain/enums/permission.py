from app.core.enums import CaseInsensitiveEnum


class PermissionModule(CaseInsensitiveEnum):
    """
    RBAC permission modules.
    """

    HOSPITALS = "HOSPITALS"
    PATIENTS = "PATIENTS"
    VITALS = "VITALS"
    TIMELINE = "TIMELINE"
    ALARMS = "ALARMS"
    ICU_MANAGEMENT = "ICU_MANAGEMENT"
    BED_MANAGEMENT = "BED_MANAGEMENT"
    DEVICE_MANAGEMENT = "DEVICE_MANAGEMENT"
    MANAGE_USERS = "MANAGE_USERS"
    DASHBOARD = "DASHBOARD"


class PermissionAction(CaseInsensitiveEnum):
    """
    RBAC permission actions.
    """

    VIEW = "VIEW"
    CREATE = "CREATE"
    MODIFY = "MODIFY"
    CANCEL = "CANCEL"
    DELETE = "DELETE"