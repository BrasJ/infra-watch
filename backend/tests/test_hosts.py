import uuid
import pytest

@pytest.fixture
def new_host(client):
    unique_hostname = f"test-{uuid.uuid4()}"
    response = client.post("/hosts", json={
        "hostname": unique_hostname,
        "ip_address": "10.0.0.1"
    })
    assert response.status_code == 200
    return response.json()

def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_create_host(client):
    unique_name = f"host-{uuid.uuid4()}"
    response = client.post('/hosts', json={
        "hostname": unique_name,
        "ip_address": "127.0.0.1"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["hostname"] == unique_name

def test_get_all_hosts(client, new_host):
    response = client.get('/hosts')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(h["id"] == new_host['id'] for h in response.json())

def test_get_single_host(client, new_host):
    response = client.get(f"/hosts/{new_host['id']}")
    assert response.status_code == 200
    assert response.json()["hostname"] == new_host["hostname"]

def test_update_host(client, new_host):
    updated_hostname = f"test-{uuid.uuid4()}"
    response = client.put(f"/hosts/{new_host['id']}", json={
        "hostname": updated_hostname,
        "ip_address": "192.168.0.100"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["hostname"] == updated_hostname
    assert data["ip_address"] == "192.168.0.100"

def test_delete_host(client, new_host):
    response = client.delete(f"/hosts/{new_host['id']}")
    assert response.status_code == 204

def test_get_deleted_hosts(client, new_host):
    client.delete(f"/hosts/{new_host['id']}")
    response = client.get(f"/hosts/{new_host['id']}")
    assert response.status_code == 404

def test_update_invalid_host(client):
    response = client.put("/hosts/9999", json={
        "hostname": f"test-{uuid.uuid4()}",
        "ip_address": "127.0.0.1"
    })
    assert response.status_code == 404

def test_delete_invalid_host(client):
    response = client.delete("/hosts/9999")
    assert response.status_code == 404