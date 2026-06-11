from fastapi import APIRouter

from app.api.v1.endpoints import (
    alarms,
    auth,
    dashboard,
    hospitals,
    ingestion,
    patients,
    timeline,
    vitals,
    clinical_notes,
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

# Admin modules
api_router.include_router(icu_management.router)
api_router.include_router(bed_management.router)
api_router.include_router(device_management.router)
api_router.include_router(user_management.router)
api_router.include_router(clinical_notes.router)