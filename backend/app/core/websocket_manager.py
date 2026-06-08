from collections import defaultdict
from datetime import datetime, timedelta, timezone
import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages active WebSocket connections for live ICU updates.

    Current support:
    - Global broadcast to all connected clients.
    - Unit-scoped broadcast to clients connected for a specific ICU/unit.
    - Heartbeat tracking for stale connection cleanup.
    - Basic connection metrics and logging.
    """

    HEARTBEAT_TIMEOUT_SECONDS = 90

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.unit_connections: dict[int, list[WebSocket]] = defaultdict(list)
        self.last_seen: dict[WebSocket, datetime] = {}

    async def connect(
        self,
        websocket: WebSocket,
    ) -> None:
        """
        Accept and register a global WebSocket client connection.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        self.mark_seen(websocket)

        logger.info(
            "WebSocket connected globally. total_connections=%s",
            self.total_connections,
        )

    async def connect_to_unit(
        self,
        websocket: WebSocket,
        unit_id: int,
    ) -> None:
        """
        Accept and register a WebSocket client connection
        for a specific ICU/unit dashboard.
        """
        await websocket.accept()
        self.unit_connections[unit_id].append(websocket)
        self.mark_seen(websocket)

        logger.info(
            "WebSocket connected to unit. unit_id=%s unit_connections=%s total_connections=%s",
            unit_id,
            self.unit_connection_count(unit_id),
            self.total_connections,
        )

    def mark_seen(
        self,
        websocket: WebSocket,
    ) -> None:
        """
        Update the last heartbeat/activity timestamp for a connection.
        """
        self.last_seen[websocket] = datetime.now(timezone.utc)

    def disconnect(
        self,
        websocket: WebSocket,
    ) -> None:
        """
        Remove a WebSocket client connection from all connection groups.
        """
        removed_from_global = False
        removed_unit_ids: list[int] = []

        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            removed_from_global = True

        for unit_id, connections in list(self.unit_connections.items()):
            if websocket in connections:
                connections.remove(websocket)
                removed_unit_ids.append(unit_id)

            if not connections:
                del self.unit_connections[unit_id]

        self.last_seen.pop(websocket, None)

        logger.info(
            "WebSocket disconnected. removed_from_global=%s removed_unit_ids=%s total_connections=%s",
            removed_from_global,
            removed_unit_ids,
            self.total_connections,
        )

    def cleanup_stale_connections(self) -> None:
        """
        Remove connections that have not sent a heartbeat recently.
        """
        now = datetime.now(timezone.utc)
        timeout_at = now - timedelta(
            seconds=self.HEARTBEAT_TIMEOUT_SECONDS
        )

        stale_connections = [
            websocket
            for websocket, last_seen_at in self.last_seen.items()
            if last_seen_at < timeout_at
        ]

        for websocket in stale_connections:
            self.disconnect(websocket)

        if stale_connections:
            logger.warning(
                "Cleaned up stale WebSocket connections. stale_count=%s total_connections=%s",
                len(stale_connections),
                self.total_connections,
            )

    async def broadcast(
        self,
        message: dict,
    ) -> None:
        """
        Broadcast an event payload to all active global WebSocket clients.
        """
        self.cleanup_stale_connections()

        logger.info(
            "Broadcasting global WebSocket event. event_type=%s recipients=%s",
            message.get("type"),
            len(self.active_connections),
        )

        await self._broadcast_to_connections(
            connections=self.active_connections,
            message=message,
        )

    async def broadcast_to_unit(
        self,
        unit_id: int,
        message: dict,
    ) -> None:
        """
        Broadcast an event payload only to clients subscribed
        to a specific ICU/unit.
        """
        self.cleanup_stale_connections()

        connections = self.unit_connections.get(
            unit_id,
            [],
        )

        logger.info(
            "Broadcasting unit WebSocket event. unit_id=%s event_type=%s recipients=%s",
            unit_id,
            message.get("type"),
            len(connections),
        )

        await self._broadcast_to_connections(
            connections=connections,
            message=message,
        )

    async def _broadcast_to_connections(
        self,
        connections: list[WebSocket],
        message: dict,
    ) -> None:
        """
        Send a message to a connection list and clean up dead sockets.
        """
        disconnected_connections: list[WebSocket] = []

        for connection in list(connections):
            try:
                await connection.send_json(message)
            except Exception:
                logger.exception(
                    "Failed to send WebSocket message. event_type=%s",
                    message.get("type"),
                )
                disconnected_connections.append(connection)

        for connection in disconnected_connections:
            self.disconnect(connection)

    @property
    def total_connections(
        self,
    ) -> int:
        """
        Return total active WebSocket connections across all groups.

        A connection can exist in either global connections or
        unit-scoped connections.
        """
        return len(self.last_seen)

    @property
    def global_connection_count(
        self,
    ) -> int:
        """
        Return active global WebSocket connection count.
        """
        return len(self.active_connections)

    def unit_connection_count(
        self,
        unit_id: int,
    ) -> int:
        """
        Return active WebSocket connection count for a unit.
        """
        return len(
            self.unit_connections.get(
                unit_id,
                [],
            )
        )

    def unit_connection_counts(
        self,
    ) -> dict[int, int]:
        """
        Return active WebSocket connection count grouped by unit.
        """
        return {
            unit_id: len(connections)
            for unit_id, connections in self.unit_connections.items()
        }


websocket_manager = WebSocketManager()