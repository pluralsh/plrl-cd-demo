from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_success_at_former_failure_timestamp():
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
