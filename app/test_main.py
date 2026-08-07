from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)
fault_client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("timestamp", [3, 4])
def test_ping_is_reliable_regardless_of_timestamp(timestamp):
    with patch("app.main.time.time", return_value=timestamp):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_synthetic_ping_fault_returns_500_at_divisible_timestamp():
    with patch("app.main.time.time", return_value=3):
        response = fault_client.get("/test/faults/ping")

    assert response.status_code == 500


def test_synthetic_ping_fault_returns_pong_at_non_divisible_timestamp():
    with patch("app.main.time.time", return_value=4):
        response = fault_client.get("/test/faults/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
