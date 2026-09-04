import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_pong_by_default_at_divisible_time():
    with patch.dict(os.environ, {}, clear=True):
        with patch("app.main.time.time", return_value=3):
            response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_raises_at_divisible_time():
    with patch.dict(os.environ, {"PING_FAULT_INJECTION": "TrUe"}):
        with patch("app.main.time.time", return_value=3):
            response = client.get("/ping")

    assert response.status_code == 500


def test_ping_fault_injection_returns_pong_at_non_divisible_time():
    with patch.dict(os.environ, {"PING_FAULT_INJECTION": "true"}):
        with patch("app.main.time.time", return_value=4):
            response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
