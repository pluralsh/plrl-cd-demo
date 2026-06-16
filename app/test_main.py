from fastapi.testclient import TestClient

from . import main

client = TestClient(main.app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy_by_default(monkeypatch):
    monkeypatch.setattr(main, "ENABLE_PING_CHAOS", False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_chaos_toggle_preserves_flaky_behavior(monkeypatch):
    monkeypatch.setattr(main, "ENABLE_PING_CHAOS", True)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    with TestClient(main.app, raise_server_exceptions=False) as test_client:
        response = test_client.get("/ping")

    assert response.status_code == 500
