def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_creat_host(client):
    response = client.post('/hosts', json={"hostname": "test-host", "ip_address": "10.0.0.1"})
    assert response.status_code == 200
    assert response.json()["hostname"] == "test-host"

def test_get_hosts(client):
    response = client.get('/hosts')
    assert response.status_code == 200
    assert isinstance(response.json(), list)