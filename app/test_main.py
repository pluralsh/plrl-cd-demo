from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)
error_client = TestClient(app, raise_server_exceptions=False)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_simulate_error():
    response = error_client.get("/simulate-error")
    assert response.status_code == 500

