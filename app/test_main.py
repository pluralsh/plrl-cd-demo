from fastapi.testclient import TestClient

from . import main
from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_stable_by_default(monkeypatch):
    monkeypatch.delenv(main.PING_FAILURE_INJECTION_ENV, raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 0)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_injection_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv(main.PING_FAILURE_INJECTION_ENV, "true")
    monkeypatch.setattr(main.time, "time", lambda: 0)

    failing_client = TestClient(app, raise_server_exceptions=False)
    response = failing_client.get("/ping")

    assert response.status_code == 500
