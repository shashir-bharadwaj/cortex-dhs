from datetime import datetime

from app.domain.enums.patient import Gender
from app.infrastructure.database.models.alarm import AlarmModel
from app.infrastructure.database.models.bed import BedMasterModel
from app.infrastructure.database.models.device_master import DeviceMasterModel
from app.infrastructure.database.models.icu_unit_master import ICUUnitMasterModel
from app.infrastructure.database.models.patient import PatientModel


def test_admin_dashboard_overview_uses_db_data(client, auth_headers, db_session, hospital):
    icu_unit = ICUUnitMasterModel(
        icu_name="MICU",
        type="Critical Care",
        department="ICU",
        beds=2,
        devices="2",
        gateway="gw-1",
        status="ACTIVE",
    )
    db_session.add(icu_unit)
    db_session.flush()

    bed = BedMasterModel(
        bed_id="BED-1",
        icu_unit_id=icu_unit.id,
        bed_type="ICU",
        department="ICU",
        ward="A",
        floor="1",
        room="101",
        cleaning_status="CLEAN",
        maintenance_status="OK",
        operational_status="ACTIVE",
    )
    db_session.add(bed)
    db_session.flush()

    patient = PatientModel(
        mrn="MRN-001",
        cr_number="CR-001",
        name="Test Patient",
        age=45,
        gender=Gender.MALE,
        bed_id=bed.id,
        diagnosis="Sepsis",
        doctor="Dr. A",
        hospital_id=hospital.id,
        status="admitted",
    )
    db_session.add(patient)
    db_session.flush()

    db_session.add(
        AlarmModel(
            patient_id=patient.id,
            patient_name=patient.name,
            bed_id=bed.bed_id,
            device="Monitor",
            message="Critical alarm",
            severity="critical",
            timestamp=datetime.utcnow(),
        )
    )
    db_session.add(
        AlarmModel(
            patient_id=patient.id,
            patient_name=patient.name,
            bed_id=bed.bed_id,
            device="Monitor",
            message="Warning alarm",
            severity="warning",
            timestamp=datetime.utcnow(),
        )
    )
    db_session.add(
        DeviceMasterModel(
            device_type="Monitor",
            manufacturer="Acme",
            model="Pro",
            serial="SER-1",
            bed_id=bed.id,
            ip_address="192.168.1.1",
            status="ACTIVE",
        )
    )
    db_session.add(
        DeviceMasterModel(
            device_type="Ventilator",
            manufacturer="Acme",
            model="Lite",
            serial="SER-2",
            bed_id=bed.id,
            ip_address="192.168.1.2",
            status="INACTIVE",
        )
    )
    db_session.commit()

    response = client.get("/api/v1/admin/dashboard/overview", headers=auth_headers)

    assert response.status_code == 200, response.text

    payload = response.json()
    assert payload["stats"]["hospitals"] == 1
    assert payload["stats"]["icuUnits"] == 1
    assert payload["stats"]["beds"] == 1
    assert payload["stats"]["patients"] == 1
    assert payload["stats"]["connected"] == 1
    assert payload["stats"]["offline"] == 1
    assert payload["stats"]["critical"] == 1
    assert payload["connectivityTrend"][0]["time"] == "00:00"
    assert payload["alertsData"][0]["critical"] >= 1
    assert payload["liveAlerts"][0]["bed"] == "BED-1"
