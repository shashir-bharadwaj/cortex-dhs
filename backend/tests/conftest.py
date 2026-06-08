import os
import asyncio
from datetime import datetime

import fastapi.routing
import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/cortex_icu_pytest.sqlite")
os.environ.setdefault("SECRET_KEY", "test_secret")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

from app.db.database import Base, get_db
from app.domain.enums.auth import ShiftType, UserRole
from app.infrastructure.database import models  # noqa: F401
from app.infrastructure.database.models.alarm import AlarmModel
from app.infrastructure.database.models.device import DeviceModel
from app.infrastructure.database.models.hospital import HospitalModel
from app.infrastructure.database.models.hospital_unit import HospitalUnitModel
from app.infrastructure.database.models.patient import PatientModel
from app.infrastructure.database.models.patient_device import PatientDevice
from app.infrastructure.database.models.role import RoleModel
from app.infrastructure.database.models.timeline import TimelineEventModel
from app.infrastructure.database.models.user import UserModel
from app.infrastructure.database.models.vital import VitalModel
from app.infrastructure.security.password_service import PasswordService
from app.main import app


async def _run_endpoint_inline(func, *args, **kwargs):
    """
    Keep sync FastAPI route handlers inline for tests.

    The current local dependency stack hangs inside the TestClient thread portal,
    so tests drive the ASGI app directly with httpx.ASGITransport.
    """
    return func(*args, **kwargs)


fastapi.routing.run_in_threadpool = _run_endpoint_inline


engine = create_engine(
    os.environ["DATABASE_URL"],
    connect_args={"check_same_thread": False},
    future=True,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    yield ASGITestClient(app)

    app.dependency_overrides.clear()


class ASGITestClient:
    """
    Small synchronous wrapper around httpx.ASGITransport.

    It keeps tests in the same request style as FastAPI TestClient while
    avoiding the local TestClient thread-portal hang for sync endpoints.
    """

    def __init__(self, test_app):
        self._app = test_app

    def request(self, method: str, url: str, **kwargs):
        async def do_request():
            transport = httpx.ASGITransport(app=self._app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://testserver",
            ) as async_client:
                return await async_client.request(method, url, **kwargs)

        return asyncio.run(do_request())

    def get(self, url: str, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs):
        return self.request("PUT", url, **kwargs)

    def patch(self, url: str, **kwargs):
        return self.request("PATCH", url, **kwargs)

    def delete(self, url: str, **kwargs):
        return self.request("DELETE", url, **kwargs)


@pytest.fixture()
def roles(db_session):
    items = {}
    for role in UserRole:
        model = RoleModel(name=role.value, description=f"{role.value.title()} role")
        db_session.add(model)
        db_session.flush()
        items[role.value] = model
    db_session.commit()
    return items


@pytest.fixture()
def hospital(db_session):
    model = HospitalModel(
        name="Test Hospital",
        code="TEST-HOSP",
        address="Test address",
        city="Bengaluru",
        state="Karnataka",
        country="India",
        contact_number="9999999999",
        email="admin@test.example",
    )
    db_session.add(model)
    db_session.flush()

    unit = HospitalUnitModel(
        hospital_id=model.id,
        name="MICU",
        code="TEST-HOSP-MICU",
        is_active=True,
    )
    db_session.add(unit)
    db_session.commit()
    db_session.refresh(model)
    return model


@pytest.fixture()
def admin_user(db_session, roles, hospital):
    unit = hospital.units[0]
    user = UserModel(
        user_id="admin",
        first_name="System",
        last_name="Admin",
        email="admin@test.example",
        password_hash=PasswordService().hash_password("admin"),
        role_id=roles[UserRole.ADMIN.value].id,
        hospital_id=str(hospital.id),
        unit_id=str(unit.id),
        shift=ShiftType.MORNING.value,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def auth_headers(client, admin_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"userId": "admin", "password": "admin"},
    )
    assert response.status_code == 200, response.text
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def patient(db_session, hospital):
    model = PatientModel(
        name="Test Patient",
        age=44,
        gender="MALE",
        bed_id="B1",
        diagnosis="Pneumonia",
        weight=70.0,
        height=170.0,
        blood_group="O+",
        doctor="Dr Test",
        admission_time=datetime.utcnow(),
        icu_unit="MICU",
        hospital_id=str(hospital.id),
        status="admitted",
        history=["Admitted for test"],
        comorbidities=["Hypertension"],
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)
    return model


@pytest.fixture()
def device(db_session):
    model = DeviceModel(
        name="Bedside Monitor",
        serial_number="MON-TEST-001",
        type="MONITOR",
        status="ONLINE",
        last_sync=datetime.utcnow(),
        location="MICU-B1",
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)
    return model


@pytest.fixture()
def patient_device(db_session, patient, device):
    model = PatientDevice(
        patient_id=patient.id,
        device_id=device.id,
        assigned_at=datetime.utcnow(),
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)
    return model


@pytest.fixture()
def vital(db_session, patient):
    model = VitalModel(
        patient_id=patient.id,
        hr=88,
        bp_sys=120,
        bp_dia=80,
        spo2=98,
        temp=98.6,
        rr=18,
        recorded_at=datetime.utcnow(),
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)
    return model


@pytest.fixture()
def timeline_event(db_session, patient):
    model = TimelineEventModel(
        patient_id=patient.id,
        type="NOTE_ADDED",
        event="Initial assessment complete",
        created_at=datetime.utcnow(),
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)
    return model


@pytest.fixture()
def alarm(db_session, patient, device):
    model = AlarmModel(
        patient_id=patient.id,
        patient_name=patient.name,
        bed_id=patient.bed_id,
        device=device.name,
        message="SpO2 warning",
        severity="Warning",
        acknowledged=False,
        silenced=False,
        escalated=False,
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)
    return model
