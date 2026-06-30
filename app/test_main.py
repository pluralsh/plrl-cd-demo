import os

from fastapi.testclient import TestClient

from . import main
from .main import app

client = TestClient(app)
erroring_client = TestClient(app, raise_server_exceptions=False)


def _refresh_ping_failure_flag():
    main.PING_FAILURE_ENABLED = os.environ.get("PING_FAILURE_ENABLED", "false").lower() in {"1", "true", "yes", "on"}


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_healthy_by_default():
    _refresh_ping_failure_flag()
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_can_fail_when_enabled(monkeypatch):
    monkeypatch.setenv("PING_FAILURE_ENABLED", "true")
    _refresh_ping_failure_flag()

    try:
        response = erroring_client.get("/ping")
        assert response.status_code == 500
    finally:
        monkeypatch.delenv("PING_FAILURE_ENABLED", raising=False)
        _refresh_ping_failure_flag()
