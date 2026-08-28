import time

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_during_former_failure_seconds(monkeypatch):
    for former_failure_second in (0, 3, 6):
        monkeypatch.setattr(time, "time", lambda: former_failure_second)

        response = client.get("/ping")

        assert response.status_code == 200
        assert response.json() == {"pong": True}
