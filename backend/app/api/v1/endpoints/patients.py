import csv
import io
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse

from app.api.providers.alarms import AlarmProvider
from app.api.providers.auth import AuthProvider
from app.api.providers.patients import PatientProvider
from app.api.schemas.alarm import AlarmResponse
from app.api.schemas.flowsheet import FlowsheetResponse
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
from app.application.patients.use_cases.get_patient_flowsheet import (
    GetPatientFlowsheetUseCase,
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


@router.get(
    "/{patient_id}/flowsheet",
    response_model=FlowsheetResponse,
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_patient_flowsheet(
    patient_id: int,
    target_date: Optional[date] = Query(default=None, alias="date"),
    _current_user=patient_permission(PermissionAction.VIEW),
    use_case: GetPatientFlowsheetUseCase = Depends(
        PatientProvider.get_flowsheet_use_case
    ),
) -> FlowsheetResponse:
    """
    Return 24-hour hourly vitals grid for the Flowsheet tab.
    Pass ?date=YYYY-MM-DD to query a specific day; defaults to today.
    """
    result = use_case.execute(patient_id=patient_id, target_date=target_date)
    return FlowsheetResponse.model_validate(result)


@router.get(
    "/{patient_id}/reports/daily-summary",
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_daily_summary(
    patient_id: int,
    _current_user=patient_permission(PermissionAction.VIEW),
    details_use_case: GetPatientDetailsUseCase = Depends(
        PatientProvider.get_patient_details_use_case
    ),
) -> dict:
    """
    Return structured patient data for printing a daily summary PDF.
    Includes patient demographics, today's vitals, and medication orders.
    """
    data = details_use_case.execute(patient_id)
    patient = data["overview"]["patient"]
    return {
        "patient": {
            "id": patient.id,
            "name": patient.name,
            "mrn": patient.mrn,
            "cr_number": patient.cr_number,
            "age": patient.age,
            "gender": patient.gender.value if patient.gender else None,
            "blood_group": patient.blood_group,
            "diagnosis": patient.diagnosis,
            "doctor": patient.doctor,
            "admission_time": (
                patient.admission_time.isoformat() if patient.admission_time else None
            ),
        },
        "latest_vitals": data["overview"]["latest_vitals"],
        "medications": data["medications"],
        "staff_assignment": data["staff_assignment"],
        "ventilator_params": data["ventilator_params"],
        "lab_data": data["lab_data"],
        "fluid_balance": data["fluid_balance"],
    }


@router.get(
    "/{patient_id}/reports/vitals-csv",
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def export_vitals_csv(
    patient_id: int,
    _current_user=patient_permission(PermissionAction.VIEW),
    flowsheet_use_case: GetPatientFlowsheetUseCase = Depends(
        PatientProvider.get_flowsheet_use_case
    ),
) -> StreamingResponse:
    """
    Stream today's 24-hour vitals as a downloadable CSV file.
    """
    result = flowsheet_use_case.execute(patient_id=patient_id)

    output = io.StringIO()
    writer = csv.writer(output)

    hours = result["hours"]
    writer.writerow(["Parameter"] + [f"{h}:00" for h in hours])
    for row in result["rows"]:
        values = [row["values"].get(str(h), "") for h in hours]
        writer.writerow([row["parameter"]] + values)

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=vitals_{patient_id}_{result['date']}.csv"
        },
    )


@router.get(
    "/{patient_id}/reports/discharge-summary",
    status_code=status.HTTP_200_OK,
    responses=STANDARD_ERROR_RESPONSES,
)
def get_discharge_summary(
    patient_id: int,
    _current_user=patient_permission(PermissionAction.VIEW),
    details_use_case: GetPatientDetailsUseCase = Depends(
        PatientProvider.get_patient_details_use_case
    ),
) -> dict:
    """
    Return structured discharge summary data (demographics, clinical notes, timeline).
    The frontend renders this into a printable document.
    """
    data = details_use_case.execute(patient_id)
    patient = data["overview"]["patient"]
    return {
        "patient": {
            "id": patient.id,
            "name": patient.name,
            "mrn": patient.mrn,
            "cr_number": patient.cr_number,
            "age": patient.age,
            "gender": patient.gender.value if patient.gender else None,
            "blood_group": patient.blood_group,
            "diagnosis": patient.diagnosis,
            "comorbidities": patient.comorbidities,
            "doctor": patient.doctor,
            "admission_time": (
                patient.admission_time.isoformat() if patient.admission_time else None
            ),
            "weight": patient.weight,
            "height": patient.height,
        },
        "vitals_summary": data["overview"]["latest_vitals"],
        "medications": data["medications"],
        "clinical_notes": data["notes"],
        "timeline": data["timeline"],
        "lab_data": data["lab_data"],
        "ventilator_params": data["ventilator_params"],
        "fluid_balance": data["fluid_balance"],
        "staff_assignment": data["staff_assignment"],
    }