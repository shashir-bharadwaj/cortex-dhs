def alarm_payload(patient, device, severity="Warning"):
    return {
        "patientId": patient.id,
        "patientName": patient.name,
        "bedId": patient.bed_id,
        "device": device.name,
        "message": "Heart rate warning",
        "severity": severity,
    }


def test_create_list_and_patient_alarm_filter(client, patient, device):
    response = client.post("/api/v1/alarms", json=alarm_payload(patient, device))

    assert response.status_code == 201
    alarm_id = response.json()["id"]

    list_response = client.get("/api/v1/alarms", params={"severity": "Warning"})
    assert list_response.status_code == 200
    assert any(item["id"] == alarm_id for item in list_response.json())

    patient_response = client.get(f"/api/v1/patients/{patient.id}/alarms")
    assert patient_response.status_code == 200
    assert any(item["id"] == alarm_id for item in patient_response.json())


def test_acknowledge_silence_and_escalate_alarm(client, alarm):
    ack_response = client.patch(
        f"/api/v1/alarms/{alarm.id}/acknowledge",
        json={"acknowledgedBy": "nurse"},
    )
    assert ack_response.status_code == 200
    assert ack_response.json()["acknowledged"] is True

    silence_response = client.patch(
        f"/api/v1/alarms/{alarm.id}/silence",
        json={"silencedBy": "nurse", "durationMinutes": 5},
    )
    assert silence_response.status_code == 200
    assert silence_response.json()["silenced"] is True

    escalate_response = client.patch(
        f"/api/v1/alarms/{alarm.id}/escalate",
        json={"escalatedBy": "nurse", "escalateTo": "doctor"},
    )
    assert escalate_response.status_code == 200
    assert escalate_response.json()["escalated"] is True


def test_silence_alarm_rejects_non_positive_duration(client, alarm):
    response = client.patch(
        f"/api/v1/alarms/{alarm.id}/silence",
        json={"silencedBy": "nurse", "durationMinutes": 0},
    )

    assert response.status_code == 400
