from fastapi import APIRouter, Depends, status

from app.api.providers.ingestion import IngestionProvider
from app.api.schemas.ingestion import (
    IngestDeviceEventsRequest,
    IngestDeviceEventsResponse,
)
from app.application.ingestion.use_cases.ingest_device_events import (
    IngestDeviceEventsUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES

router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)


@router.post(
    "/device-events",
    response_model=IngestDeviceEventsResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
async def ingest_device_events(
    payload: IngestDeviceEventsRequest,
    use_case: IngestDeviceEventsUseCase = Depends(
        IngestionProvider.ingest_device_events_use_case
    ),
) -> IngestDeviceEventsResponse:
    """
    Ingest canonical device events from the Edge SDK.
    """
    result = await use_case.execute(
        payload.events
    )

    return IngestDeviceEventsResponse(
        **result
    )