from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy_without_chaos_testing(monkeypatch):
    monkeypatch.delenv("ENABLE_CHAOS_TESTING", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3.0)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_returns_500_when_chaos_testing_is_enabled(monkeypatch):
    monkeypatch.setenv("ENABLE_CHAOS_TESTING", "true")
    monkeypatch.setattr(main.time, "time", lambda: 3.0)
    chaos_client = TestClient(main.app, raise_server_exceptions=False)

    response = chaos_client.get("/ping")

    assert response.status_code == 500
