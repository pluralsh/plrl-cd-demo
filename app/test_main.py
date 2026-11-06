from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)
failure_client = TestClient(main.app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_by_default(monkeypatch):
    monkeypatch.delenv("PING_FAILURE_ENABLED", raising=False)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_can_be_enabled(monkeypatch):
    monkeypatch.setenv("PING_FAILURE_ENABLED", "true")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = failure_client.get("/ping")

    assert response.status_code == 500
