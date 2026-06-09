from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fail_preserves_demo_fault_injection(monkeypatch):
    monkeypatch.setattr("app.main.time.time", lambda: 3)

    response = client.get("/ping/fail")

    assert response.status_code == 500
