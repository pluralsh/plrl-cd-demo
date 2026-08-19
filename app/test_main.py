import time
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("timestamp", [1.0, 2.0, 3.0, 6.0])
def test_ping_returns_pong_regardless_of_current_timestamp(timestamp):
    failure_response_client = TestClient(app, raise_server_exceptions=False)

    with patch.object(time, "time", return_value=timestamp):
        response = failure_response_client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
