from app.core.enums import CaseInsensitiveEnum


class MedicationOrderType(CaseInsensitiveEnum):
    PRN = "PRN"
    STAT = "STAT"
    INFUSION = "Infusion"


class MedicationStatus(CaseInsensitiveEnum):
    PENDING = "Pending"
    RUNNING = "Running"
    GIVEN = "Given"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
