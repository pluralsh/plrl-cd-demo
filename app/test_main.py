from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_by_default(monkeypatch):
    monkeypatch.delenv("PING_FAIL_ENABLED", raising=False)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_is_explicitly_opt_in(monkeypatch):
    monkeypatch.setenv("PING_FAIL_ENABLED", "true")
    failure_client = TestClient(app, raise_server_exceptions=False)

    response = failure_client.get("/ping")

    assert response.status_code == 500
