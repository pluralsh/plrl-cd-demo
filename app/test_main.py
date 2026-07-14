from fastapi.testclient import TestClient
from unittest.mock import patch

from .main import app

client = TestClient(app)
no_raise_client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_demo_failure_can_still_fail():
    with patch("app.main.time.time", return_value=3):
        response = no_raise_client.get("/demo/failure")
    assert response.status_code == 500


def test_demo_failure_can_succeed():
    with patch("app.main.time.time", return_value=4):
        response = no_raise_client.get("/demo/failure")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
