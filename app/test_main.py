from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_pong():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_is_stable_across_requests():
    statuses = [client.get("/ping").status_code for _ in range(5)]
    assert statuses == [200, 200, 200, 200, 200]
