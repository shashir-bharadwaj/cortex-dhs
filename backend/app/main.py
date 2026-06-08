# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.api.v1.endpoints.websocket import websocket_router
from app.core.config import settings
from app.core.errors import register_exception_handlers

tags_metadata = [
    {
        "name": "Patients",
        "description": "Operations related to ICU patient management.",
    },
    {
        "name": "Vitals",
        "description": "Patient vital sign recording and retrieval.",
    },
    {
        "name": "Timeline",
        "description": "Patient activity and event history.",
    },
    {
        "name": "Devices",
        "description": "Device inventory and patient-device assignment flows.",
    },
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Backend API for Cortex ICU patient monitoring workflows.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dev only. Restrict this for production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global exception handling before adding routes.
register_exception_handlers(app)

# REST API routes.
app.include_router(api_router, prefix=settings.API_V1_STR)

# WebSocket routes.
app.include_router(websocket_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Cortex ICU Backend running"}