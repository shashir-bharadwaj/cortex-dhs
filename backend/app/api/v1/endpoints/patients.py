from typing import List

from fastapi import APIRouter, Depends, status

from app.api.providers.alarms import AlarmProvider
from app.api.providers.auth import AuthProvider
from app.api.providers.patients import PatientProvider
from app.api.schemas.alarm import AlarmResponse
from app.api.schemas.patient import (
    PatientCreateRequest,
    PatientDetailResponse,
    PatientResponse,
    PatientUpdateRequest,
)
from app.api.schemas.patient_details import PatientDetailsResponse
from app.application.alarms.use_cases.get_patient_alarms import (
    GetPatientAlarmsUseCase,
)
from app.application.patients.use_cases.create_patient import (
    CreatePatientUseCase,
)
from app.application.patients.use_cases.discharge_patient import (
    DischargePatientUseCase,
)
from app.application.patients.use_cases.get_patient import GetPatientUseCase
from app.application.patients.use_cases.get_patient_details import (
    GetPatientDetailsUseCase,
)
from app.application.patients.use_cases.list_patients import (
    ListPatientsUseCase,
)
from app.application.patients.use_cases.update_patient import (
    UpdatePatientUseCase,
)
from app.core.errors.docs import STANDARD_ERROR_RESPONSES
from app.domain.entities.patient import Patient
from app.domain.enums.permission import (
    PermissionAction,
    PermissionModule,
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


def patient_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for Patient routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.PATIENTS,
            action,
        )
    )


def alarm_permission(action: PermissionAction):
    """
    Build reusable RBAC dependency for Alarm routes.
    """
    return Depends(
        AuthProvider.permission_dependency(
            PermissionModule.ALARMS,
            action,
        )
    )


def to_patient_response(patient) -> PatientResponse:
    """
    Convert patient entity into API response schema.
    """
    return PatientResponse.model_validate(patient)


def to_patient_detail_response(patient) -> PatientDetailResponse:
    """
    Convert patient detail entity into API response schema.
    """
    return PatientDetailResponse.model_validate(patient)


def to_patient_details_response(
    payload: dict,
) -> PatientDetailsResponse:
    """
    Convert patient details aggregation payload into API response schema.
    """
    return PatientDetailsResponse.model_validate(payload)


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    responses=STANDARD_ERROR_RESPONSES,
)
def create_patient(
    payload: PatientCreateRequest,
    _current_user=patient_permission(PermissionAction.CREATE),
    use_case: CreatePatientUseCase = Depends(
        PatientProvider.get_create_patient_use_case
    ),
) -> PatientResponse:
    """
    Create a new patient admission record.
    """
    patient = Patient(
        name=payload.name,
        age=payload.age,
        gender=payload.gender,
        bed_id=payload.bed_id,
        diagnosis=payload.diagnosis,
        weight=payload.weight,
        height=payload.height,
        blood_group=payload.blood_group,
        doctor=payload.doctor,
        admission_time=payload.admission_time,
        hospital_id=payload.hospital_id,
        history=payload.history,
        comorbidities=payload.comorbidities,
    )

    patient = use_case.execute(patient)

    return to_patient_response(patient)


@router.get(
    "",
    response_model=List[PatientResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def list_patients(
    _current_user=patient_permission(PermissionAction.VIEW),
    use_case: ListPatientsUseCase = Depends(
        PatientProvider.get_list_patients_use_case
    ),
) -> List[PatientResponse]:
    """
    List all patients.
    """
    patients = use_case.execute()

    return [
        to_patient_response(patient)
        for patient in patients
    ]


@router.get(
    "/{patient_id}/details",
    response_model=PatientDetailsResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_patient_details(
    patient_id: int,
    _current_user=patient_permission(PermissionAction.VIEW),
    use_case: GetPatientDetailsUseCase = Depends(
        PatientProvider.get_patient_details_use_case
    ),
) -> PatientDetailsResponse:
    """
    Fetch complete patient details required by the Patient Details screen.
    """
    result = use_case.execute(patient_id)

    return to_patient_details_response(result)


@router.get(
    "/{patient_id}",
    response_model=PatientDetailResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_patient(
    patient_id: int,
    _current_user=patient_permission(PermissionAction.VIEW),
    use_case: GetPatientUseCase = Depends(
        PatientProvider.get_get_patient_use_case
    ),
) -> PatientDetailResponse:
    """
    Fetch detailed patient information.
    """
    patient = use_case.execute(patient_id)

    return to_patient_detail_response(patient)


@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def update_patient(
    patient_id: int,
    payload: PatientUpdateRequest,
    _current_user=patient_permission(PermissionAction.MODIFY),
    use_case: UpdatePatientUseCase = Depends(
        PatientProvider.get_update_patient_use_case
    ),
) -> PatientResponse:
    """
    Update patient details and admission metadata.
    """
    patient = Patient(
        name=payload.name,
        age=payload.age,
        gender=payload.gender,
        bed_id=payload.bed_id,
        diagnosis=payload.diagnosis,
        weight=payload.weight,
        height=payload.height,
        blood_group=payload.blood_group,
        doctor=payload.doctor,
        admission_time=payload.admission_time,
        hospital_id=payload.hospital_id,
        history=payload.history,
        comorbidities=payload.comorbidities,
    )

    patient = use_case.execute(
        patient_id=patient_id,
        patient=patient,
    )

    return to_patient_response(patient)


@router.post(
    "/{patient_id}/discharge",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def discharge_patient(
    patient_id: int,
    _current_user=patient_permission(PermissionAction.CANCEL),
    use_case: DischargePatientUseCase = Depends(
        PatientProvider.get_discharge_patient_use_case
    ),
) -> PatientResponse:
    """
    Discharge a patient from the ICU workflow.
    """
    patient = use_case.execute(patient_id)

    return to_patient_response(patient)


@router.get(
    "/{patient_id}/alarms",
    response_model=list[AlarmResponse],
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_patient_alarms(
    patient_id: int,
    acknowledged: bool | None = None,
    _current_user=alarm_permission(PermissionAction.VIEW),
    use_case: GetPatientAlarmsUseCase = Depends(
        AlarmProvider.get_patient_alarms_use_case
    ),
):
    """
    Fetch alarms associated with a patient.
    """
    return use_case.execute(
        patient_id=patient_id,
        acknowledged=acknowledged,
    )