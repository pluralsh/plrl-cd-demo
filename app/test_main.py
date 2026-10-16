import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from . import main



def test_read_root():
    response = TestClient(main.app).get("/")
    assert response.status_code == 200


def test_ping_succeeds_without_fault_injection():
    with patch.dict(os.environ, {"PING_FAULT_INJECTION": ""}):
        with patch.object(main.time, "time", return_value=0):
            response = TestClient(main.app).get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_fault_injection_returns_server_error():
    with patch.dict(os.environ, {"PING_FAULT_INJECTION": "true"}):
        with patch.object(main.time, "time", return_value=0):
            response = TestClient(main.app, raise_server_exceptions=False).get("/ping")

    assert response.status_code == 500
