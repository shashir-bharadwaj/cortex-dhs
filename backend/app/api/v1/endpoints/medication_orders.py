from typing import List

from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.providers.medication_order import MedicationOrderProvider
from app.api.schemas.medication_order import (
    MedicationOrderCreateRequest,
    MedicationOrderResponse,
)
from app.application.medication.use_cases.create_medication_order import (
    CreateMedicationOrderUseCase,
)
from app.application.medication.use_cases.list_medication_orders import (
    ListMedicationOrdersUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(prefix="/patients", tags=["Medication Orders"])


def patient_permission(action: PermissionAction):
    return Depends(
        AuthProvider.permission_dependency(PermissionModule.PATIENTS, action)
    )


@router.post(
    "/{patient_id}/medications",
    response_model=MedicationOrderResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_medication_order(
    patient_id: int,
    payload: MedicationOrderCreateRequest,
    current_user=patient_permission(PermissionAction.CREATE),
    use_case: CreateMedicationOrderUseCase = Depends(
        MedicationOrderProvider.get_create_use_case
    ),
) -> MedicationOrderResponse:
    """
    Create a medication order for a patient.
    """
    order = use_case.execute(
        patient_id=patient_id,
        drug_name=payload.drug_name,
        order_type=payload.order_type,
        dose=payload.dose,
        route=payload.route,
        schedule=payload.schedule,
        status=payload.status,
        rate_ml_hr=payload.rate_ml_hr,
        remaining_vol_ml=payload.remaining_vol_ml,
        est_end_time=payload.est_end_time,
    )
    return MedicationOrderResponse.model_validate(order)


@router.get(
    "/{patient_id}/medications",
    response_model=List[MedicationOrderResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_medication_orders(
    patient_id: int,
    current_user=patient_permission(PermissionAction.VIEW),
    use_case: ListMedicationOrdersUseCase = Depends(
        MedicationOrderProvider.get_list_use_case
    ),
) -> List[MedicationOrderResponse]:
    """
    Return all medication orders for a patient.
    """
    orders = use_case.execute(patient_id=patient_id)
    return [MedicationOrderResponse.model_validate(o) for o in orders]
