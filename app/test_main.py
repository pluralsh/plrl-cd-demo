from fastapi.testclient import TestClient

from .main import PING_FAULT_INJECTION_ENV, app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_by_default(monkeypatch):
    monkeypatch.delenv(PING_FAULT_INJECTION_ENV, raising=False)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv(PING_FAULT_INJECTION_ENV, "true")

    response = TestClient(app, raise_server_exceptions=False).get("/ping")

    assert response.status_code == 500
