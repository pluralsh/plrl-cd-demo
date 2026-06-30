from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_stable_by_default(monkeypatch):
    monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_can_be_enabled(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "true")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    assert main.should_fail_ping() is True
