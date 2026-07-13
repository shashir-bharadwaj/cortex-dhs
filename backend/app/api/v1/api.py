from fastapi import APIRouter

from app.api.v1.endpoints import (
    alarms,
    auth,
    clinical_notes,
    dashboard as core_dashboard,
    fluid_balance,
    handover,
    hospitals,
    ingestion,
    lab_results,
    medication_orders,
    nurse_tasks,
    patients,
    timeline,
    ventilator_settings,
    vitals,
)

from app.api.v1.endpoints.admin import (
    audit_logs,
    bed_management,
    cloud_sync,
    connectivity,
    dashboard as admin_dashboard,
    device_management,
    icu_management,
    reports,
    settings,
    user_management,
)

api_router = APIRouter()

# Core modules
api_router.include_router(auth.router)
api_router.include_router(patients.router)
api_router.include_router(vitals.router)
api_router.include_router(timeline.router)
api_router.include_router(hospitals.router)
api_router.include_router(alarms.router)
api_router.include_router(connectivity.router)
api_router.include_router(settings.router)
api_router.include_router(core_dashboard.router)
api_router.include_router(ingestion.router)
api_router.include_router(clinical_notes.router)

# Clinical modules
api_router.include_router(ventilator_settings.router)
api_router.include_router(lab_results.router)
api_router.include_router(fluid_balance.router)
api_router.include_router(medication_orders.patients_router)
api_router.include_router(medication_orders.router)

# Operational modules
api_router.include_router(nurse_tasks.router)
api_router.include_router(handover.router)

# Admin modules
api_router.include_router(audit_logs.router)
api_router.include_router(cloud_sync.router)
api_router.include_router(cloud_sync.router)
api_router.include_router(reports.router)
api_router.include_router(admin_dashboard.router)
api_router.include_router(icu_management.router)
api_router.include_router(bed_management.router)
api_router.include_router(device_management.router)
api_router.include_router(user_management.router)