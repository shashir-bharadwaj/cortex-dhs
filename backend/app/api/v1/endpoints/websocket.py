from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.websocket_manager import websocket_manager

router = APIRouter()

websocket_router = router


@router.websocket("/ws/live-vitals")
async def live_vitals_websocket(
    websocket: WebSocket,
):
    """
    Global live vitals WebSocket stream.

    All connected clients receive all live vital/alarm updates.

    URL:
    ws://localhost:8000/api/v1/ws/live-vitals
    """
    await websocket_manager.connect(websocket)

    try:
        while True:
            # Any received message is treated as client activity.
            # Frontend can send "ping" periodically to keep the socket alive.
            await websocket.receive_text()
            websocket_manager.mark_seen(websocket)

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

    except Exception:
        websocket_manager.disconnect(websocket)


@router.websocket("/ws/live-vitals/{unit_id}")
async def live_vitals_unit_websocket(
    websocket: WebSocket,
    unit_id: int,
):
    """
    ICU/unit-scoped live vitals WebSocket stream.

    Only clients subscribed to the given ICU/unit receive updates
    for that unit.

    URL:
    ws://localhost:8000/api/v1/ws/live-vitals/1
    """
    await websocket_manager.connect_to_unit(
        websocket=websocket,
        unit_id=unit_id,
    )

    try:
        while True:
            # Any received message is treated as client activity.
            # Frontend can send "ping" periodically to keep the socket alive.
            await websocket.receive_text()
            websocket_manager.mark_seen(websocket)

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

    except Exception:
        websocket_manager.disconnect(websocket)