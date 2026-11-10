from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("timestamp", [0, 3, 1_700_000_001])
def test_ping_succeeds_at_previously_failing_time_boundaries(timestamp):
    with patch("time.time", return_value=timestamp):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
