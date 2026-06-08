from typing import List

from fastapi import APIRouter, Depends, status

from app.api.providers.admin.device_management import (
    DeviceManagementProvider,
)
from app.api.providers.auth import AuthProvider
from app.api.schemas.device_master import (
    DeviceMasterCreateRequest,
    DeviceMasterResponse,
    DeviceMasterUpdateRequest,
)
from app.application.device_management.use_cases.assign_device_to_bed import (
    AssignDeviceToBedUseCase,
)
from app.application.device_management.use_cases.create_device_master import (
    CreateDeviceMasterUseCase,
)
from app.application.device_management.use_cases.delete_device_master import (
    DeleteDeviceMasterUseCase,
)
from app.application.device_management.use_cases.list_device_masters import (
    ListDeviceMastersUseCase,
)
from app.application.device_management.use_cases.list_devices_by_bed import (
    ListDevicesByBedUseCase,
)
from app.application.device_management.use_cases.read_device_master import (
    ReadDeviceMasterUseCase,
)
from app.application.device_management.use_cases.unassign_device_from_bed import (
    UnassignDeviceFromBedUseCase,
)
from app.application.device_management.use_cases.update_device_master import (
    UpdateDeviceMasterUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)

router = APIRouter(
    prefix="/admin/devices",
    tags=["Admin - Device Management"],
)


def device_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for Device Management routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.DEVICE_MANAGEMENT,
            action,
        )
    )


@router.post(
    "",
    response_model=DeviceMasterResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_device(
    payload: DeviceMasterCreateRequest,
    _current_user=device_permission(PermissionAction.CREATE),
    use_case: CreateDeviceMasterUseCase = Depends(
        DeviceManagementProvider.create_device_master_use_case
    ),
):
    """
    Register a new device.
    """
    return use_case.execute(payload)


@router.get(
    "",
    response_model=List[DeviceMasterResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_devices(
    _current_user=device_permission(PermissionAction.VIEW),
    use_case: ListDeviceMastersUseCase = Depends(
        DeviceManagementProvider.list_device_masters_use_case
    ),
):
    """
    List all registered devices.
    """
    return use_case.execute()


@router.get(
    "/{device_record_id}",
    response_model=DeviceMasterResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def read_device(
    device_record_id: int,
    _current_user=device_permission(PermissionAction.VIEW),
    use_case: ReadDeviceMasterUseCase = Depends(
        DeviceManagementProvider.read_device_master_use_case
    ),
):
    """
    Read a single registered device.
    """
    return use_case.execute(device_record_id)


@router.put(
    "/{device_record_id}",
    response_model=DeviceMasterResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def update_device(
    device_record_id: int,
    payload: DeviceMasterUpdateRequest,
    _current_user=device_permission(PermissionAction.MODIFY),
    use_case: UpdateDeviceMasterUseCase = Depends(
        DeviceManagementProvider.update_device_master_use_case
    ),
):
    """
    Update device registration details.
    """
    return use_case.execute(device_record_id, payload)


@router.delete(
    "/{device_record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=STANDARD_ERROR_RESPONSES,
)
def delete_device(
    device_record_id: int,
    _current_user=device_permission(PermissionAction.DELETE),
    use_case: DeleteDeviceMasterUseCase = Depends(
        DeviceManagementProvider.delete_device_master_use_case
    ),
):
    """
    Delete a registered device.
    """
    use_case.execute(device_record_id)

    return None


@router.patch(
    "/{device_record_id}/assign-bed/{bed_id}",
    response_model=DeviceMasterResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def assign_device_to_bed(
    device_record_id: int,
    bed_id: int,
    _current_user=device_permission(PermissionAction.MODIFY),
    use_case: AssignDeviceToBedUseCase = Depends(
        DeviceManagementProvider.assign_device_to_bed_use_case
    ),
):
    """
    Map a device to a bed.
    """
    return use_case.execute(device_record_id, bed_id)


@router.patch(
    "/{device_record_id}/unassign-bed",
    response_model=DeviceMasterResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def unassign_device_from_bed(
    device_record_id: int,
    _current_user=device_permission(PermissionAction.MODIFY),
    use_case: UnassignDeviceFromBedUseCase = Depends(
        DeviceManagementProvider.unassign_device_from_bed_use_case
    ),
):
    """
    Remove the device-to-bed mapping.
    """
    return use_case.execute(device_record_id)


@router.get(
    "/by-bed/{bed_id}",
    response_model=List[DeviceMasterResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_devices_by_bed(
    bed_id: int,
    _current_user=device_permission(PermissionAction.VIEW),
    use_case: ListDevicesByBedUseCase = Depends(
        DeviceManagementProvider.list_devices_by_bed_use_case
    ),
):
    """
    List all devices mapped to a specific bed.
    """
    return use_case.execute(bed_id)