from fastapi import APIRouter, Depends, status

from app.api.providers.auth import AuthProvider
from app.api.providers.hospital import HospitalProvider
from app.api.schemas.hospital import (
    CreateHospitalRequest,
    CreateHospitalUnitRequest,
    HospitalDetailResponse,
    HospitalListItemResponse,
    HospitalUnitResponse,
    HospitalUnitsResponse,
)
from app.application.hospital.use_cases.create_hospital import (
    CreateHospitalUseCase,
)
from app.application.hospital.use_cases.create_hospital_unit import (
    CreateHospitalUnitUseCase,
)
from app.application.hospital.use_cases.get_hospital import (
    GetHospitalUseCase,
)
from app.application.hospital.use_cases.get_hospital_unit import (
    GetHospitalUnitUseCase,
)
from app.application.hospital.use_cases.list_hospitals import (
    ListHospitalsUseCase,
)
from app.application.hospital.use_cases.list_units_by_hospital import (
    ListUnitsByHospitalUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)

router = APIRouter(
    prefix="/hospitals",
    tags=["Hospitals"],
)


def hospital_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for Hospital routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.HOSPITALS,
            action,
        )
    )


@router.post(
    "",
    response_model=HospitalDetailResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_hospital(
    payload: CreateHospitalRequest,
    _current_user=hospital_permission(
        PermissionAction.CREATE
    ),
    use_case: CreateHospitalUseCase = Depends(
        HospitalProvider.get_create_hospital_use_case
    ),
) -> HospitalDetailResponse:
    """
    Create a new hospital.
    """
    return use_case.execute(
        name=payload.name,
        code=payload.code,
        address=payload.address,
        city=payload.city,
        state=payload.state,
        country=payload.country,
        contact_number=payload.contact_number,
        email=payload.email,
    )


@router.get(
    "",
    response_model=list[HospitalListItemResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_hospitals(
    _current_user=hospital_permission(
        PermissionAction.VIEW
    ),
    use_case: ListHospitalsUseCase = Depends(
        HospitalProvider.get_list_hospitals_use_case
    ),
) -> list[HospitalListItemResponse]:
    """
    List all hospitals.
    """
    return use_case.execute()


@router.get(
    "/units/{unit_id}",
    response_model=HospitalUnitResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_hospital_unit(
    unit_id: int,
    _current_user=hospital_permission(
        PermissionAction.VIEW
    ),
    use_case: GetHospitalUnitUseCase = Depends(
        HospitalProvider.get_get_hospital_unit_use_case
    ),
) -> HospitalUnitResponse:
    """
    Fetch a hospital unit by ID.
    """
    return use_case.execute(unit_id)


@router.get(
    "/{hospital_id}",
    response_model=HospitalDetailResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_hospital(
    hospital_id: int,
    _current_user=hospital_permission(
        PermissionAction.VIEW
    ),
    use_case: GetHospitalUseCase = Depends(
        HospitalProvider.get_get_hospital_use_case
    ),
) -> HospitalDetailResponse:
    """
    Fetch detailed hospital information.
    """
    return use_case.execute(hospital_id)


@router.post(
    "/{hospital_id}/units",
    response_model=HospitalUnitResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_hospital_unit(
    hospital_id: int,
    payload: CreateHospitalUnitRequest,
    _current_user=hospital_permission(
        PermissionAction.CREATE
    ),
    use_case: CreateHospitalUnitUseCase = Depends(
        HospitalProvider.get_create_hospital_unit_use_case
    ),
) -> HospitalUnitResponse:
    """
    Create a new hospital unit under a hospital.
    """
    return use_case.execute(
        hospital_id=hospital_id,
        name=payload.name,
        code=payload.code,
    )


@router.get(
    "/{hospital_id}/units",
    response_model=HospitalUnitsResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_units_by_hospital(
    hospital_id: int,
    _current_user=hospital_permission(
        PermissionAction.VIEW
    ),
    use_case: ListUnitsByHospitalUseCase = Depends(
        HospitalProvider.get_list_units_by_hospital_use_case
    ),
) -> HospitalUnitsResponse:
    """
    List all units belonging to a hospital.
    """
    units = use_case.execute(hospital_id)

    return {"units": units}