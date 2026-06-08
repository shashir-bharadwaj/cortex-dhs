def test_list_get_and_list_hospital_units(client, hospital):
    list_response = client.get("/api/v1/hospitals")
    assert list_response.status_code == 200
    assert list_response.json() == [{"id": hospital.id, "name": hospital.name}]

    get_response = client.get(f"/api/v1/hospitals/{hospital.id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == hospital.name
    assert get_response.json()["units"] == ["MICU"]

    units_response = client.get(f"/api/v1/hospitals/{hospital.id}/units")
    assert units_response.status_code == 200
    assert units_response.json() == {"units": ["MICU"]}


def test_get_hospital_not_found(client):
    response = client.get("/api/v1/hospitals/9999")

    assert response.status_code == 404
