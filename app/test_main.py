from fastapi.testclient import TestClient

from . import main



def test_read_root():
    response = TestClient(main.app).get("/")
    assert response.status_code == 200


def test_ping_is_healthy_by_default(monkeypatch):
    monkeypatch.delenv("ENABLE_FLAKY_PING", raising=False)
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = TestClient(main.app).get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_can_be_made_flaky_explicitly(monkeypatch):
    monkeypatch.setenv("ENABLE_FLAKY_PING", "true")
    monkeypatch.setattr(main.time, "time", lambda: 3)

    response = TestClient(main.app, raise_server_exceptions=False).get("/ping")

    assert response.status_code == 500
