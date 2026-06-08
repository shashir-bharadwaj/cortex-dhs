from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.alarm import AlarmSeverity


@dataclass
class Alarm:
    """
    Domain entity representing an ICU alarm.

    Business meaning:
    - active alarm raised for a patient/device
    - can be acknowledged, silenced, and escalated
    """

    id: int | None
    timestamp: datetime

    patient_id: int
    patient_name: str
    bed_id: str
    device: str

    message: str
    severity: AlarmSeverity

    acknowledged: bool = False
    silenced: bool = False
    escalated: bool = False

    acknowledged_by: str | None = None
    silenced_by: str | None = None
    silence_until: datetime | None = None

    escalated_by: str | None = None
    escalate_to: str | None = None