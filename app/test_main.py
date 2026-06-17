from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)
failure_client = TestClient(main.app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy_by_default(monkeypatch):
    monkeypatch.setattr(main, "FAIL_PING_FOR_DEMO", False)
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setattr(main, "FAIL_PING_FOR_DEMO", True)
    monkeypatch.setattr(main.time, "time", lambda: 3)
    response = failure_client.get("/ping")
    assert response.status_code == 500
