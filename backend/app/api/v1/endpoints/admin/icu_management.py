from typing import List

from fastapi import APIRouter, Depends, status

from app.api.providers.admin.icu_management import ICUManagementProvider
from app.api.providers.auth import AuthProvider
from app.api.schemas.icu_unit_master import (
    ICUUnitMasterCreateRequest,
    ICUUnitMasterResponse,
    ICUUnitMasterUpdateRequest,
)
from app.application.icu_management.use_cases.create_icu_unit import (
    CreateICUUnitUseCase,
)
from app.application.icu_management.use_cases.delete_icu_unit import (
    DeleteICUUnitUseCase,
)
from app.application.icu_management.use_cases.list_icu_units import (
    ListICUUnitsUseCase,
)
from app.application.icu_management.use_cases.read_icu_unit import (
    ReadICUUnitUseCase,
)
from app.application.icu_management.use_cases.update_icu_unit import (
    UpdateICUUnitUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)

router = APIRouter(
    prefix="/admin/icu-units",
    tags=["Admin - ICU Management"],
)


def icu_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for ICU Management routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.ICU_MANAGEMENT,
            action,
        )
    )


@router.post(
    "",
    response_model=ICUUnitMasterResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_icu_unit(
    payload: ICUUnitMasterCreateRequest,
    _current_user=icu_permission(PermissionAction.CREATE),
    use_case: CreateICUUnitUseCase = Depends(
        ICUManagementProvider.create_icu_unit_use_case
    ),
):
    """
    Create a new ICU unit.
    """
    return use_case.execute(payload)


@router.get(
    "",
    response_model=List[ICUUnitMasterResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_icu_units(
    _current_user=icu_permission(PermissionAction.VIEW),
    use_case: ListICUUnitsUseCase = Depends(
        ICUManagementProvider.list_icu_units_use_case
    ),
):
    """
    List all ICU units.
    """
    return use_case.execute()


@router.get(
    "/{icu_unit_id}",
    response_model=ICUUnitMasterResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def read_icu_unit(
    icu_unit_id: int,
    _current_user=icu_permission(PermissionAction.VIEW),
    use_case: ReadICUUnitUseCase = Depends(
        ICUManagementProvider.read_icu_unit_use_case
    ),
):
    """
    Read a single ICU unit by record ID.
    """
    return use_case.execute(icu_unit_id)


@router.put(
    "/{icu_unit_id}",
    response_model=ICUUnitMasterResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def update_icu_unit(
    icu_unit_id: int,
    payload: ICUUnitMasterUpdateRequest,
    _current_user=icu_permission(PermissionAction.MODIFY),
    use_case: UpdateICUUnitUseCase = Depends(
        ICUManagementProvider.update_icu_unit_use_case
    ),
):
    """
    Update ICU unit configuration and metadata.
    """
    return use_case.execute(icu_unit_id, payload)


@router.delete(
    "/{icu_unit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=STANDARD_ERROR_RESPONSES,
)
def delete_icu_unit(
    icu_unit_id: int,
    _current_user=icu_permission(PermissionAction.DELETE),
    use_case: DeleteICUUnitUseCase = Depends(
        ICUManagementProvider.delete_icu_unit_use_case
    ),
):
    """
    Delete an ICU unit by record ID.
    """
    use_case.execute(icu_unit_id)

    return None