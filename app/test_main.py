import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import PING_FAULT_INJECTION_ENV, app

client = TestClient(app)
error_client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy_by_default():
    with patch.dict(os.environ, {}, clear=False):
        with patch("app.main.time.time", return_value=3):
            response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_can_be_enabled():
    with patch.dict(os.environ, {PING_FAULT_INJECTION_ENV: "true"}, clear=False):
        with patch("app.main.time.time", return_value=3):
            response = error_client.get("/ping")

    assert response.status_code == 500
