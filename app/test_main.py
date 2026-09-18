from fastapi.testclient import TestClient
from unittest.mock import patch

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_reliable_by_default(monkeypatch):
    monkeypatch.delenv("PING_FAILURE_ENABLED", raising=False)

    # Exercise the second that previously raised the injected exception.
    with patch("app.main.time.time", return_value=3):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_failure_injection_requires_explicit_opt_in(monkeypatch):
    monkeypatch.setenv("PING_FAILURE_ENABLED", "true")
    failure_client = TestClient(app, raise_server_exceptions=False)

    with patch("app.main.time.time", return_value=3):
        response = failure_client.get("/ping")

    assert response.status_code == 500
