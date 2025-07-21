import uuid
import pytest
from app.schemas.alert import AlertSeverity

@pytest.fixture
def host_for_alert(client):
    response = client.post("/hosts", json={
        "hostname": f"host-{uuid.uuid4()}",
        "ip_address": "10.0.0.1"
    })
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def snapshot_for_alert(client, host_for_alert):
    response = client.post("/snapshots", json={
        "host_id": host_for_alert["id"],
    })
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def alert_fixture(client, snapshot_for_alert):
    response = client.post("/alerts", json={
        "snapshot_id": snapshot_for_alert["id"],
        "message": "CPU usage high",
        "severity": "warning",
        "type": "system",
        "acknowledged": False
    })
    assert response.status_code == 200
    return response.json()

def test_create_alert(client, snapshot_for_alert):
    response = client.post("/alerts", json={
        "snapshot_id": snapshot_for_alert["id"],
        "message": "Disk full",
        "severity": "critical",
        "type": "system",
        "acknowledged": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Disk full"
    assert data["severity"] == "critical"
    assert data["acknowledged"] is False

def test_get_alerts(client, alert_fixture):
    response = client.get(f"/alerts/{alert_fixture['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "CPU usage high"

def test_list_alerts(client, alert_fixture):
    response = client.get("/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(a["id"] == alert_fixture["id"] for a in response.json())

def test_filter_alerts_by_ack(client, alert_fixture):
    response = client.get("/alerts", params={"acknowledged": False})
    assert response.status_code == 200
    assert all(alert["acknowledged"] is False for alert in response.json())

def test_filter_alerts_by_severity(client, alert_fixture):
    response = client.get("/alerts", params={"severity": "warning"})
    assert response.status_code == 200
    assert all(alert["severity"] == "warning" for alert in response.json())

def test_update_alert(client, alert_fixture):
    response = client.put(f"/alerts/{alert_fixture['id']}", json={
        "acknowledged": True
    })
    assert response.status_code == 200
    assert response.json()["acknowledged"]

def test_delete_alert(client, alert_fixture):
    response = client.delete(f"/alerts/{alert_fixture['id']}")
    assert response.status_code == 204

def test_get_deleted_alert(client, alert_fixture):
    client.delete(f"/alerts/{alert_fixture['id']}")
    response = client.get(f"/alerts/{alert_fixture['id']}")
    assert response.status_code == 404