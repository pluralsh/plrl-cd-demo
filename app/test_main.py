from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_without_fault_injection(monkeypatch):
    monkeypatch.delenv("PING_FAULT_INJECTION", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_requires_explicit_true(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "true")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 500


def test_ping_ignores_malformed_fault_injection(monkeypatch):
    monkeypatch.setenv("PING_FAULT_INJECTION", "yes")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
