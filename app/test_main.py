import time

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_remains_healthy_when_clock_would_have_triggered_fault(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 3)

    response = client.get("/ping")

    assert int(time.time()) % 3 == 0
    assert response.status_code == 200
    assert response.json() == {"pong": True}
