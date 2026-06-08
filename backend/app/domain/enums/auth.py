from app.core.enums import CaseInsensitiveEnum


class UserRole(CaseInsensitiveEnum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    TECHNICIAN = "TECHNICIAN"


class ShiftType(CaseInsensitiveEnum):
    MORNING = "MORNING"
    EVENING = "EVENING"
    NIGHT = "NIGHT"