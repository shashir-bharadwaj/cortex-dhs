"""
Websocket manager for real-time streaming of vital data and alerts.
"""

from typing import List
from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Simple connection manager to handle websocket clients."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_vital(self, vital):
        data = {
            "type": "vital",
            "patient_id": vital.patient_id,
            "device_id": vital.device_id,
            "vital_type": vital.vital_type,
            "value": float(vital.value),
            "recorded_at": vital.recorded_at.isoformat(),
        }
        await self.broadcast(data)

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                # client disconnected
                self.disconnect(connection)


manager = ConnectionManager()