from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_when_fault_injection_is_not_enabled(monkeypatch):
    monkeypatch.delenv(main.PING_FAULT_INJECTION_ENABLED, raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 6)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_injects_fault_when_explicitly_enabled(monkeypatch):
    monkeypatch.setenv(main.PING_FAULT_INJECTION_ENABLED, "true")
    monkeypatch.setattr(main.time, "time", lambda: 6)

    response = client.get("/ping")

    assert response.status_code == 500
    assert response.json() == {"detail": "demo ping fault injection enabled"}
