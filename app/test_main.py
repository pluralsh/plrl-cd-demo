from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_without_error_injection(monkeypatch):
    monkeypatch.delenv("PING_ERROR_INJECTION", raising=False)
    monkeypatch.setattr("app.main.time.time", lambda: 3)

    for _ in range(3):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}


def test_ping_error_injection_is_opt_in(monkeypatch):
    monkeypatch.setenv("PING_ERROR_INJECTION", "true")
    monkeypatch.setattr("app.main.time.time", lambda: 3)

    response = TestClient(app, raise_server_exceptions=False).get("/ping")
    assert response.status_code == 500
