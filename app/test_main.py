from fastapi.testclient import TestClient

from . import main


client = TestClient(main.app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_when_fault_injection_is_not_enabled(monkeypatch):
    monkeypatch.delenv(main.PING_FAILURE_ENABLED_ENV, raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_is_explicit_and_deterministic(monkeypatch):
    monkeypatch.setenv(main.PING_FAILURE_ENABLED_ENV, "true")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = TestClient(main.app, raise_server_exceptions=False).get("/ping")

    assert response.status_code == 500
