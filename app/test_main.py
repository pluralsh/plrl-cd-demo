from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_without_failure_opt_in(monkeypatch):
    monkeypatch.delenv("PING_FAIL_ENABLED", raising=False)
    monkeypatch.setattr("app.main.time.time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_simulation_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv("PING_FAIL_ENABLED", "true")
    monkeypatch.setattr("app.main.time.time", lambda: 3)
    error_client = TestClient(app, raise_server_exceptions=False)

    response = error_client.get("/ping")

    assert response.status_code == 500
