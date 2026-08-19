from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy_by_default(monkeypatch):
    monkeypatch.delenv("ENABLE_CHAOS_TESTING", raising=False)

    with patch("app.main.time.time", return_value=3.0):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_injection_requires_opt_in(monkeypatch):
    monkeypatch.setenv("ENABLE_CHAOS_TESTING", "true")
    failure_client = TestClient(app, raise_server_exceptions=False)

    with patch("app.main.time.time", return_value=3.0):
        response = failure_client.get("/ping")

    assert response.status_code == 500
