from enum import Enum


class AlarmSeverity(str, Enum):
    """
    Alarm severity values supported by the ICU API spec.
    """

    CRITICAL = "Critical"
    WARNING = "Warning"
    INFO = "Info"