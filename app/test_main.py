from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_reliable_by_default(monkeypatch):
    monkeypatch.delenv(main.PING_FAILURE_INJECTION_ENV, raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_fixture_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv(main.PING_FAILURE_INJECTION_ENV, "true")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 500
