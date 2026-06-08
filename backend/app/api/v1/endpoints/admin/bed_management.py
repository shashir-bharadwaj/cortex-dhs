from typing import List

from fastapi import APIRouter, Depends, status

from app.api.providers.admin.bed_management import BedManagementProvider
from app.api.providers.auth import AuthProvider
from app.api.schemas.bed_master import (
    BedMasterCreateRequest,
    BedMasterResponse,
    BedMasterUpdateRequest,
)
from app.application.bed_management.use_cases.create_bed import CreateBedUseCase
from app.application.bed_management.use_cases.delete_bed import DeleteBedUseCase
from app.application.bed_management.use_cases.list_beds import ListBedsUseCase
from app.application.bed_management.use_cases.read_bed import ReadBedUseCase
from app.application.bed_management.use_cases.update_bed import UpdateBedUseCase
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import PermissionAction, PermissionModule

router = APIRouter(
    prefix="/admin/beds",
    tags=["Admin - Bed Management"],
)


def bed_permission(action: PermissionAction):
    """
    Build a reusable permission dependency for Bed Management routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.BED_MANAGEMENT,
            action,
        )
    )


@router.post(
    "",
    response_model=BedMasterResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_bed(
    payload: BedMasterCreateRequest,
    _current_user=bed_permission(PermissionAction.CREATE),
    use_case: CreateBedUseCase = Depends(
        BedManagementProvider.create_bed_use_case
    ),
):
    """
    Create a bed and map it to an ICU unit.
    """
    return use_case.execute(payload)


@router.get(
    "",
    response_model=List[BedMasterResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_beds(
    _current_user=bed_permission(PermissionAction.VIEW),
    use_case: ListBedsUseCase = Depends(
        BedManagementProvider.list_beds_use_case
    ),
):
    """
    List all beds.
    """
    return use_case.execute()


@router.get(
    "/{bed_record_id}",
    response_model=BedMasterResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def read_bed(
    bed_record_id: int,
    _current_user=bed_permission(PermissionAction.VIEW),
    use_case: ReadBedUseCase = Depends(
        BedManagementProvider.read_bed_use_case
    ),
):
    """
    Read a single bed by record ID.
    """
    return use_case.execute(bed_record_id)


@router.put(
    "/{bed_record_id}",
    response_model=BedMasterResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def update_bed(
    bed_record_id: int,
    payload: BedMasterUpdateRequest,
    _current_user=bed_permission(PermissionAction.MODIFY),
    use_case: UpdateBedUseCase = Depends(
        BedManagementProvider.update_bed_use_case
    ),
):
    """
    Update bed details and ICU unit mapping.
    """
    return use_case.execute(bed_record_id, payload)


@router.delete(
    "/{bed_record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=STANDARD_ERROR_RESPONSES,
)
def delete_bed(
    bed_record_id: int,
    _current_user=bed_permission(PermissionAction.DELETE),
    use_case: DeleteBedUseCase = Depends(
        BedManagementProvider.delete_bed_use_case
    ),
):
    """
    Delete a bed by record ID.
    """
    use_case.execute(bed_record_id)
    return None