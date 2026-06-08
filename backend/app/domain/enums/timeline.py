from app.core.enums import CaseInsensitiveEnum


class TimelineEventType(CaseInsensitiveEnum):
    """
    Enum representing all supported timeline event types.
    """

    DEVICE_ASSIGNED = "DEVICE_ASSIGNED"
    DEVICE_REMOVED = "DEVICE_REMOVED"
    STATUS_CHANGED = "STATUS_CHANGED"
    NOTE_ADDED = "NOTE_ADDED"