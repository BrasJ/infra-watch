import uuid
import pytest

@pytest.fixture
def new_metric(client):
    snapshot_id = 1     # TODO: Change when snapshot support implemented
    name = f"cpu-{uuid.uuid4()}"
    response = client.post("/metrics", json={
        "snapshot_id": snapshot_id,
        "name": name,
        "value": 42.0,
        "unit": "%",
        "description": "CPU usage"
    })
    assert response.status_code == 200
    return response.json()

def test_create_metric(client):
    name = f"mem-{uuid.uuid4()}"
    response = client.post("/metrics", json={
        "snapshot_id": 1,
        "name": name,
        "value": 84.0,
        "unit": "%",
        "description": "Memory usage"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"].startswith("mem-")

def test_get_metric(client, new_metric):
    response = client.get(f"/metrics/{new_metric['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == new_metric["name"]

def test_list_metrics_by_snapshot(client, new_metric):
    response = client.get(f"/metrics/snapshot/{new_metric['snapshot_id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_metric(client, new_metric):
    response = client.delete(f"/metrics/{new_metric['id']}")
    assert response.status_code == 204

def test_get_deleted_metric(client, new_metric):
    del_response = client.delete(f"/metrics/{new_metric['id']}")
    assert del_response.status_code == 204

    response = client.get(f"/metrics/{new_metric['id']}")
    assert response.status_code == 404