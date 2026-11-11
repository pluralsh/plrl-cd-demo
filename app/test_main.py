import time

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_at_previously_failing_epoch(monkeypatch):
    formerly_failing_epoch = 1_700_000_001
    assert formerly_failing_epoch % 3 == 0
    monkeypatch.setattr(time, "time", lambda: formerly_failing_epoch)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
