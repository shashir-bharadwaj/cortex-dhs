"""
Device-related domain enums.

These enums:
- Accept case-insensitive input
- Store canonical uppercase values
- Are used across API, application, and persistence layers
"""

from app.core.enums import CaseInsensitiveEnum


class DeviceType(CaseInsensitiveEnum):
    """
    Supported ICU device categories.
    """

    MONITOR = "MONITOR"
    VENTILATOR = "VENTILATOR"
    ECG = "ECG"
    SPO2 = "SPO2"
    PUMP = "PUMP"
    TEMPERATURE = "TEMPERATURE"
    INFUSION_PUMP = "INFUSION_PUMP"


class DeviceStatus(CaseInsensitiveEnum):
    """
    Operational status of a device.
    """

    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    WARNING = "WARNING"