from fastapi import APIRouter

from app.api.v1.endpoints import (
    alarms,
    auth,
    clinical_notes,
    dashboard,
    fluid_balance,
    hospitals,
    ingestion,
    lab_results,
    medication_orders,
    patients,
    timeline,
    ventilator_settings,
    vitals,
)

from app.api.v1.endpoints.admin import (
    bed_management,
    device_management,
    icu_management,
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
api_router.include_router(dashboard.router)
api_router.include_router(ingestion.router)
api_router.include_router(clinical_notes.router)

# Clinical modules
api_router.include_router(ventilator_settings.router)
api_router.include_router(lab_results.router)
api_router.include_router(fluid_balance.router)
api_router.include_router(medication_orders.router)

# Admin modules
api_router.include_router(icu_management.router)
api_router.include_router(bed_management.router)
api_router.include_router(device_management.router)
api_router.include_router(user_management.router)