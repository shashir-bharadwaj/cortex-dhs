def test_create_and_list_patient_vitals(client, auth_headers, patient):
    response = client.post(
        f"/api/v1/patients/{patient.id}/vitals",
        headers=auth_headers,
        json={
            "hr": 90,
            "bp_sys": 120,
            "bp_dia": 80,
            "spo2": 98,
            "temp": 98.6,
            "rr": 18,
        },
    )

    assert response.status_code == 201
    vital_id = response.json()["id"]

    list_response = client.get(
        f"/api/v1/patients/{patient.id}/vitals",
        headers=auth_headers,
    )
    assert list_response.status_code == 200
    assert any(item["id"] == vital_id for item in list_response.json())

    get_response = client.get(
        f"/api/v1/patients/{patient.id}/vitals/{vital_id}",
        headers=auth_headers,
    )
    assert get_response.status_code == 200
    assert get_response.json()["hr"] == 90


def test_create_vital_for_missing_patient_returns_404(client, auth_headers):
    response = client.post(
        "/api/v1/patients/9999/vitals",
        headers=auth_headers,
        json={"hr": 90},
    )

    assert response.status_code == 404


def test_create_and_list_timeline(client, auth_headers, patient):
    response = client.post(
        f"/api/v1/patients/{patient.id}/timeline",
        headers=auth_headers,
        json={"event": "Doctor reviewed", "type": "NOTE_ADDED"},
    )

    assert response.status_code == 201
    assert response.json()["event"] == "Doctor reviewed"

    list_response = client.get(
        f"/api/v1/patients/{patient.id}/timeline",
        headers=auth_headers,
    )
    assert list_response.status_code == 200
    assert any(item["event"] == "Doctor reviewed" for item in list_response.json())


def test_timeline_for_missing_patient_returns_404(client, auth_headers):
    response = client.get("/api/v1/patients/9999/timeline", headers=auth_headers)

    assert response.status_code == 404
