import uuid
import pytest

@pytest.fixture
def host_for_snapshot(client):
    hostname = f"host-{uuid.uuid4()}"
    response = client.post("/hosts", json={
        "hostname": hostname,
        "ip_address": "10.0.0.1"
    })
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def snapshot(client, host_for_snapshot):
    response = client.post("/snapshots", json={"host_id": host_for_snapshot["id"]})
    assert response.status_code == 200
    return response.json()

def test_create_snapshot(client, host_for_snapshot):
    response = client.post("/snapshots", json={"host_id": host_for_snapshot["id"]})
    assert response.status_code == 200
    data = response.json()
    assert data["host_id"] == host_for_snapshot["id"]

def test_get_snapshot(client, snapshot):
    response = client.get(f"/snapshots/{snapshot['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == snapshot["id"]

def test_list_snapshots(client, host_for_snapshot, snapshot):
    response = client.get(f"/snapshots/hosts/{host_for_snapshot['id']}")
    assert response.status_code == 200
    snapshots = response.json()
    assert isinstance(snapshots, list)
    assert any(s["id"] == snapshot["id"] for s in snapshots)

def test_delete_snapshot(client, snapshot):
    response = client.delete(f"/snapshots/{snapshot['id']}")
    assert response.status_code == 204

def test_get_deleted_snapshot(client, snapshot):
    client.delete(f"/snapshots/{snapshot['id']}")
    response = client.get(f"/snapshots/{snapshot['id']}")
    assert response.status_code == 404