def icu_payload(name="MICU-A"):
    return {
        "icu_name": name,
        "type": "MICU",
        "department": "Critical Care",
        "beds": 10,
        "devices": "Monitor,Ventilator",
        "gateway": "GW-1",
        "status": "ACTIVE",
    }


def bed_payload(bed_id="BED-A"):
    return {
        "bed_id": bed_id,
        "bed_type": "ICU",
        "department": "Critical Care",
        "ward": "MICU",
        "floor": "1",
        "room": "101",
        "cleaning_status": "CLEAN",
        "maintenance_status": "OK",
        "operational_status": "AVAILABLE",
    }


def device_master_payload(serial="DM-A"):
    return {
        "device_type": "Monitor",
        "manufacturer": "Generic",
        "model": "M100",
        "serial": serial,
        "bed": "BED-A",
        "ip_address": "10.0.0.10",
        "status": "ACTIVE",
    }


def test_admin_icu_unit_crud(client):
    create_response = client.post("/api/v1/admin/icu-units", json=icu_payload())
    assert create_response.status_code == 201
    icu_id = create_response.json()["id"]

    duplicate_response = client.post("/api/v1/admin/icu-units", json=icu_payload())
    assert duplicate_response.status_code == 409

    list_response = client.get("/api/v1/admin/icu-units")
    assert list_response.status_code == 200
    assert any(item["id"] == icu_id for item in list_response.json())

    read_response = client.get(f"/api/v1/admin/icu-units/{icu_id}")
    assert read_response.status_code == 200

    update_response = client.put(
        f"/api/v1/admin/icu-units/{icu_id}",
        json=icu_payload(name="MICU-B"),
    )
    assert update_response.status_code == 200
    assert update_response.json()["icu_name"] == "MICU-B"

    delete_response = client.delete(f"/api/v1/admin/icu-units/{icu_id}")
    assert delete_response.status_code == 204


def test_admin_bed_crud(client):
    create_response = client.post("/api/v1/admin/beds", json=bed_payload())
    assert create_response.status_code == 201
    bed_id = create_response.json()["id"]

    duplicate_response = client.post("/api/v1/admin/beds", json=bed_payload())
    assert duplicate_response.status_code == 409

    list_response = client.get("/api/v1/admin/beds")
    assert list_response.status_code == 200
    assert any(item["id"] == bed_id for item in list_response.json())

    read_response = client.get(f"/api/v1/admin/beds/{bed_id}")
    assert read_response.status_code == 200

    update_response = client.put(
        f"/api/v1/admin/beds/{bed_id}",
        json=bed_payload(bed_id="BED-B"),
    )
    assert update_response.status_code == 200
    assert update_response.json()["bed_id"] == "BED-B"

    delete_response = client.delete(f"/api/v1/admin/beds/{bed_id}")
    assert delete_response.status_code == 204


def test_admin_device_master_crud(client):
    create_response = client.post(
        "/api/v1/admin/devices",
        json=device_master_payload(),
    )
    assert create_response.status_code == 201
    device_id = create_response.json()["id"]

    duplicate_response = client.post(
        "/api/v1/admin/devices",
        json=device_master_payload(),
    )
    assert duplicate_response.status_code == 409

    list_response = client.get("/api/v1/admin/devices")
    assert list_response.status_code == 200
    assert any(item["id"] == device_id for item in list_response.json())

    read_response = client.get(f"/api/v1/admin/devices/{device_id}")
    assert read_response.status_code == 200

    update_response = client.put(
        f"/api/v1/admin/devices/{device_id}",
        json=device_master_payload(serial="DM-B"),
    )
    assert update_response.status_code == 200
    assert update_response.json()["serial"] == "DM-B"

    delete_response = client.delete(f"/api/v1/admin/devices/{device_id}")
    assert delete_response.status_code == 204
