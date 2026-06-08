def device_payload(serial_number="MON-NEW-001"):
    return {
        "name": "New Monitor",
        "serial_number": serial_number,
        "type": "MONITOR",
        "status": "ONLINE",
        "location": "MICU-B4",
    }


def test_create_list_get_update_and_status_device(client, auth_headers):
    create_response = client.post(
        "/api/v1/devices",
        headers=auth_headers,
        json=device_payload(),
    )
    assert create_response.status_code == 201
    device_id = create_response.json()["id"]

    list_response = client.get("/api/v1/devices", headers=auth_headers)
    assert list_response.status_code == 200
    assert any(item["id"] == device_id for item in list_response.json())

    get_response = client.get(f"/api/v1/devices/{device_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["serial_number"] == "MON-NEW-001"

    update_response = client.put(
        f"/api/v1/devices/{device_id}",
        headers=auth_headers,
        json={"name": "Updated Monitor", "location": "MICU-B5"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Monitor"

    status_response = client.patch(
        f"/api/v1/devices/{device_id}/status",
        headers=auth_headers,
        json={"status": "WARNING", "error": "Low battery"},
    )
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "WARNING"
    assert status_response.json()["error"] == "Low battery"


def test_create_device_duplicate_serial_returns_409(client, auth_headers, device):
    response = client.post(
        "/api/v1/devices",
        headers=auth_headers,
        json=device_payload(serial_number=device.serial_number),
    )

    assert response.status_code == 409


def test_assign_list_and_remove_device_from_patient(client, auth_headers, patient, device):
    assign_response = client.post(
        f"/api/v1/patients/{patient.id}/devices",
        headers=auth_headers,
        json={"deviceId": device.id},
    )
    assert assign_response.status_code == 201
    assert assign_response.json()["deviceId"] == device.id

    list_response = client.get(
        f"/api/v1/patients/{patient.id}/devices",
        headers=auth_headers,
    )
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    delete_response = client.delete(
        f"/api/v1/patients/{patient.id}/devices/{device.id}",
        headers=auth_headers,
    )
    assert delete_response.status_code == 204

    list_after_delete = client.get(
        f"/api/v1/patients/{patient.id}/devices",
        headers=auth_headers,
    )
    assert list_after_delete.status_code == 200
    assert list_after_delete.json() == []


def test_assign_already_assigned_device_returns_400(
    client,
    auth_headers,
    patient,
    patient_device,
):
    response = client.post(
        f"/api/v1/patients/{patient.id}/devices/{patient_device.device_id}",
        headers=auth_headers,
    )

    assert response.status_code == 400
