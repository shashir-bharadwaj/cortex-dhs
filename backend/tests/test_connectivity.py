def test_get_connectivity_payload(client):
    response = client.get("/api/v1/connectivity")

    assert response.status_code == 200
    payload = response.json()

    assert "summary" in payload
    assert "timeline" in payload
    assert "devices" in payload

    assert payload["summary"]["online"] == 7
    assert payload["summary"]["offline"] == 3
    assert payload["summary"]["dataRate"] == "1.2 Gbps"

    assert len(payload["timeline"]) == 7
    assert len(payload["devices"]) == 9
    assert payload["devices"][0]["id"] == "DEV-001"
