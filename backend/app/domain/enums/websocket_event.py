# app/domain/enums/websocket_event.py

from enum import Enum


class WebSocketEventType(str, Enum):
    """
    WebSocket event types emitted by Cortex ICU.

    These values are sent to frontend clients through
    live ICU WebSocket streams.
    """

    LIVE_VITAL_UPDATE = "LIVE_VITAL_UPDATE"
    LIVE_ALARM_UPDATE = "LIVE_ALARM_UPDATE"
    DEVICE_STATUS_UPDATE = "DEVICE_STATUS_UPDATE"