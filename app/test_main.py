import time

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_ping_returns_pong_at_former_failure_epoch(monkeypatch):
    # Epoch second 0 is divisible by three and triggered the removed exception.
    monkeypatch.setattr(time, "time", lambda: 0)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
