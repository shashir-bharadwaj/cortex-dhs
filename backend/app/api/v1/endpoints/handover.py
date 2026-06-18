from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.providers.handover import HandoverProvider
from app.api.schemas.handover import ShiftHandoverResponse
from app.application.handover.use_cases.get_shift_summary import GetShiftSummaryUseCase
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(prefix="/handover", tags=["Handover"])


@router.get(
    "/shift-summary",
    response_model=ShiftHandoverResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_shift_summary(
    current_user=Depends(
        AuthProvider.permission_dependency(PermissionModule.PATIENTS, PermissionAction.VIEW)
    ),
    use_case: GetShiftSummaryUseCase = Depends(HandoverProvider.get_shift_summary_use_case),
) -> ShiftHandoverResponse:
    """Return aggregated per-patient handover summary for the current shift."""
    return use_case.execute()
