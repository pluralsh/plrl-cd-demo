from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)
non_raising_client = TestClient(app, raise_server_exceptions=False)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_ok_by_default():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_can_still_fail_in_demo_mode(monkeypatch):
    monkeypatch.setenv("PING_FAIL_MODE", "always")
    response = non_raising_client.get("/ping")
    assert response.status_code == 500
    monkeypatch.delenv("PING_FAIL_MODE", raising=False)
