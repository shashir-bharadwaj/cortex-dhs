def patient_payload(name="Created Patient", bed_id="B9"):
    return {
        "name": name,
        "age": 50,
        "gender": "MALE",
        "bedId": bed_id,
        "diagnosis": "Sepsis",
        "weight": 72.5,
        "height": 171.0,
        "bloodGroup": "O+",
        "doctor": "Dr Test",
        "icuUnit": "MICU",
        "hospitalId": "1",
        "history": ["Admitted"],
        "comorbidities": ["Diabetes"],
    }


def test_create_patient(client, auth_headers):
    response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json=patient_payload(),
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Created Patient"
    assert response.json()["bedId"] == "B9"


def test_create_patient_validates_required_name(client, auth_headers):
    payload = patient_payload()
    payload.pop("name")

    response = client.post("/api/v1/patients", headers=auth_headers, json=payload)

    assert response.status_code == 422


def test_list_and_get_patient(client, auth_headers, patient, vital, patient_device, timeline_event):
    list_response = client.get("/api/v1/patients", headers=auth_headers)
    assert list_response.status_code == 200
    assert any(item["id"] == patient.id for item in list_response.json())

    detail_response = client.get(f"/api/v1/patients/{patient.id}", headers=auth_headers)
    assert detail_response.status_code == 200
    body = detail_response.json()
    assert body["name"] == patient.name
    assert body["vitals"]
    assert body["devices"]
    assert body["timeline"]


def test_get_patient_not_found(client, auth_headers):
    response = client.get("/api/v1/patients/9999", headers=auth_headers)

    assert response.status_code == 404


def test_update_and_discharge_patient(client, auth_headers, patient):
    response = client.put(
        f"/api/v1/patients/{patient.id}",
        headers=auth_headers,
        json=patient_payload(name="Updated Patient", bed_id="B2"),
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Patient"

    discharge_response = client.post(
        f"/api/v1/patients/{patient.id}/discharge",
        headers=auth_headers,
    )

    assert discharge_response.status_code == 200
    assert discharge_response.json()["status"] == "discharged"
