import importlib

from fastapi.testclient import TestClient

from . import main


client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy_by_default(monkeypatch):
    monkeypatch.delenv(main.PING_FAILURE_MODE_ENV, raising=False)
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_can_fail_when_demo_mode_enabled(monkeypatch):
    monkeypatch.setenv(main.PING_FAILURE_MODE_ENV, main.PING_FAILURE_MODE_DEMO)
    response = client.get("/ping")
    assert response.status_code == 500
    assert response.json() == {"detail": "intentional demo failure mode enabled"}


def test_ping_failure_mode_check_is_case_insensitive(monkeypatch):
    monkeypatch.setenv(main.PING_FAILURE_MODE_ENV, " DeMo ")
    assert main.ping_failure_mode_enabled() is True
